import hashlib
import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import SimpleLazyObject


class TemplateStorage:
	def __init__(self):
		if getattr(settings, 'TEMPLATES', None):
			template_dirs = [d for source in settings.TEMPLATES for d in source.get('DIRS', [])]
		else:
			template_dirs = settings.TEMPLATE_DIRS

		templates = []
		template_for_key = {}
		for top_dir in template_dirs:
			for walked_dir, subdirs, files in os.walk(top_dir):
				for f in files:
					# Example:
					# top_dir = /www/app/templates
					# walked_dir = /www/app/templates/accounts
					# f = login.html
					# path = /www/app/templates/accounts/login.html
					# relative_path = accounts/login.html
					path = os.path.join(walked_dir, f)
					relative_path = path[len(top_dir)+1:]
					key = hashlib.md5(path.encode()).hexdigest()
					template = Template(key=key, top_dir=top_dir, relative_path=relative_path)
					template_for_key[key] = template
					templates.append(template)

		# TODO: order templates

		self.templates = templates
		self.template_for_key = template_for_key

templates_storage = SimpleLazyObject(TemplateStorage)


class TemplateQuerySet(models.QuerySet):
	def iterator(self):
		return templates_storage.templates

	def count(self):
		return len(templates_storage.templates)

	def get(self, key):
		try:
			return templates_storage.template_for_key[key]
		except KeyError:
			raise Template.DoesNotExist

	def delete(self):
		raise NotImplementedError


class Template(models.Model):
	class Meta:
		managed = False

	key = models.CharField(max_length=32, primary_key=True, editable=False)
	top_dir = models.CharField("Directory", max_length=255, editable=False)
	relative_path = models.CharField("Template", max_length=255, editable=False)
	content = models.TextField(blank=True)

	objects = TemplateQuerySet.as_manager()

	def __str__(self):
		return self.path

	@property
	def path(self):
		return os.path.join(self.top_dir, self.relative_path)

	def clean(self):
		try:
			with open(self.path, 'a'):
				pass
		except Exception as e:
			raise ValidationError(e)

	def is_editable(self):
		return os.access(self.path, os.W_OK)
	is_editable.boolean = True
	is_editable.short_description = "Editable"

	def load_content(self):
		self.content = self.read_content()

	def read_content(self):
		return open(self.path, 'r', newline='').read()  # preserve EOLs

	def fix_eols(self):
		"""
		Convert to Unix EOLs unless the original file was Windows encoded.
		"""
		old_content = self.read_content()
		rn_pos = old_content.find('\r\n')
		if rn_pos >= 0 and rn_pos < old_content.find('\n'):
			# Do not fix EOLs if the first EOL in the old content was \r\n
			return

		self.content = self.content.replace('\r\n', '\n')

	def save(self, *args, **kwargs):
		open(self.path, 'w').write(self.content)
