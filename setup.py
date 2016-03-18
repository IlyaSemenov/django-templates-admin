# coding=utf-8
from setuptools import setup, find_packages

"""
This Django app allows to edit Django project template files from within the Django administrative interface.
"""

setup(
	name='django-templates-admin',
	version='0.3.0',
	url='https://github.com/IlyaSemenov/django-templates-admin',
	license='BSD',
	author='Ilya Semenov',
	author_email='ilya@semenov.co',
	description='Edit project template files from the Django admin UI',
	long_description=__doc__,
	packages=find_packages(),
	include_package_data=True,
	zip_safe=False,
	platforms='any',
	install_requires=[],
	classifiers=[],
)
