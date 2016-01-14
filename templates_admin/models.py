import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import SimpleLazyObject


def _find_templates():
	if getattr(settings, 'TEMPLATES', None):
		template_dirs = [d for source in settings.TEMPLATES for d in source.get('DIRS', [])]
	else:
		template_dirs = settings.TEMPLATE_DIRS

	templates = []
	for top_dir in template_dirs:
		for root, dirs, files in os.walk(top_dir):
			for f in files:
				templates.append(Template(path=os.path.join(root, f), top_dir=top_dir))
	return templates

all_templates = SimpleLazyObject(_find_templates)


class TemplateQuerySet(models.QuerySet):
	def iterator(self):
		return all_templates

	def count(self):
		return len(all_templates)

	def get(self, path):
		templates = list(filter(lambda t: t.path == path, all_templates))
		if not templates:
			raise Template.DoesNotExist
		return templates[0]

	def delete(self):
		pass


class Template(models.Model):
	class Meta:
		managed = False

	path = models.CharField(max_length=255, primary_key=True, editable=False)
	top_dir = models.CharField("Directory", max_length=255, editable=False)
	content = models.TextField(blank=True)

	objects = TemplateQuerySet.as_manager()

	def __str__(self):
		return self.path

	def clean(self):
		try:
			with open(self.path, 'a'):
				pass
		except Exception as e:
			raise ValidationError(e)

	@property
	def relative_name(self):
		return self.path[len(self.top_dir)+1:]

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
