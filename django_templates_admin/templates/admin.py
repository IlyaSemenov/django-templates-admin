from django.contrib import admin
from .models import Template


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
	list_display = 'relative_path', 'top_dir', 'is_editable'
	actions = None

	fields = 'top_dir', 'relative_path', 'content'
	readonly_fields = 'top_dir', 'relative_path'

	def has_add_permission(self, request):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def get_object(self, *args, **kwargs):
		template = super().get_object(*args, **kwargs)
		if template:
			template.load_content()
		return template

	def save_model(self, request, obj, form, change):
		obj.fix_eols()
		obj.save()
