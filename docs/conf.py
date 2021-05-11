import jsonscribe

project = 'jsonscribe'
copyright = 'AWeber Communications, Inc'
release = '.'.join(str(c) for c in jsonscribe.version_info[:2])
version = jsonscribe.version
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]
source_suffix = '.rst'
master_doc = 'index'
html_static_path = ['.']
html_theme = 'alabaster'
html_sidebars = {'**': ['about.html', 'navigation.html', 'searchbox.html']}
intersphinx_mapping = {
    'python': ('http://docs.python.org/3/', None),
}
