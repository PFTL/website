import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

project = 'My Module'
copyright = '2018, Aquiles Carattino'
author = 'Aquiles Carattino'
version = ''
release = '0.1'
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
pygments_style = 'sphinx'
html_theme = 'alabaster'
html_static_path = ['_static']
extensions = [
    'sphinx.ext.autodoc',]