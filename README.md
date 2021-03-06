django-templates-admin
======================

This Django app allows to edit Django project template files from within the Django administrative interface.

Installation
------------

```
pip install django-templates-admin
```

Usage
-----

Add the application to `settings.py`:

```python
INSTALLED_APPS =
    ...
    'django_templates_admin.templates',
```

On the main admin page, a new section **Templates** will appear:

![The list of templates](https://raw.githubusercontent.com/IlyaSemenov/django-templates-admin/master/screenshots/list.png)

Click on a template to edit it:

![Editing a template](https://raw.githubusercontent.com/IlyaSemenov/django-templates-admin/master/screenshots/form.png)
