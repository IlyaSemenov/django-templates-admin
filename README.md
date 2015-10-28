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
    'templates_admin.apps.TemplatesAdminConfig',  # Django 1.7+
    'templates_admin',  # Django 1.6 and earlier
```

On the main admin page, a new section **Templates** will appear.
