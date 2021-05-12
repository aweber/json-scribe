import jsonscribe

project = 'jsonscribe'
copyright = 'AWeber Communications, Inc'
release = '.'.join(str(c) for c in jsonscribe.version_info[:2])
version = jsonscribe.version
source_suffix = '.rst'
master_doc = 'index'
html_extra_path = ['../CODE_OF_CONDUCT.md']
html_static_path = ['.']
html_theme = 'alabaster'
html_sidebars = {'**': ['about.html', 'navigation.html', 'searchbox.html']}
extensions = []

# see https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
extensions.append('sphinx.ext.intersphinx')
intersphinx_mapping = {
    'python': ('http://docs.python.org/3/', None),
}

# see https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
extensions.append('sphinx.ext.autodoc')

# see https://www.sphinx-doc.org/en/master/usage/extensions/extlinks.html
extensions.append('sphinx.ext.extlinks')
extlinks = {
    'compare': ('https://github.com/aweber/json-scribe/compare/%s', ''),
}
