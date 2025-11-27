# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'User Authentication service'
copyright = '2025, Nalongsone Danddank'
author = 'Nalongsone Danddank'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# import os
# import sys
# sys.path.insert(0, os.path.abspath('..'))          # repo root
# sys.path.insert(0, os.path.abspath('../accountService'))  # Django project package
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accountService.settings')
# import django
# django.setup()

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
