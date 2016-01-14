from django.contrib import admin
from .models import Template


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
	list_display = 'get_relative_name', 'top_dir'
	actions = None

	fields = 'top_dir', 'get_relative_name', 'content'
	readonly_fields = 'top_dir', 'get_relative_name',

	def has_add_permission(self, request):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def get_relative_name(self, template):
		return template.relative_name
	get_relative_name.short_description = "Template"

	def get_object(self, *args, **kwargs):
		template = super().get_object(*args, **kwargs)
		template.load_content()
		return template

	def save_model(self, request, obj, form, change):
		obj.fix_eols()
		obj.save()
