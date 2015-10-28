import os

from django.conf import settings
from django.db import models
from django.utils.functional import SimpleLazyObject


def _find_templates():
	templates = []
	# TODO: make this compatible with old-style settings.TEMPLATE_DIRS
	for engine in settings.TEMPLATES:
		for top_dir in engine['DIRS']:
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

	@property
	def relative_name(self):
		return self.path[len(self.top_dir)+1:]

	def load_content(self):
		self.content = open(self.path, 'r').read()

	def save(self, *args, **kwargs):
		open(self.path, 'w').write(self.content)
