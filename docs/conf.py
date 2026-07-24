import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'CARE Semantic Model — Version 2'
copyright = ''
author = 'Pablo Alarcon Moreno, Mark D. Wilkinson'

extensions = ['myst_parser', 'sphinxcontrib.mermaid']
source_suffix = {
    '.md': 'markdown',
}
master_doc = 'index'

myst_fence_as_directive = ["mermaid"]

language = 'en'
html_logo = 'assets/care-sm.png'
html_theme = 'sphinx_rtd_theme'
html_static_path = ["_static"]
html_favicon = "_static/favicon.png"
html_static_path = ['_static']

mermaid_version = "10.9.1"

def setup(app):
    app.add_css_file('custom.css')
