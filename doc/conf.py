# -*- coding: utf-8 -*-
#

import os

import sphinx
if sphinx.version_info < (5, 2):
    import warnings
    warnings.warn("You should use sphinx 5.2+")


# monkey patch https://github.com/sphinx-doc/sphinx/issues/11253
def split(self, input):
    res = []
    for word in sphinx.search.SearchLanguage.split(self, input):
        res.extend(word.split("_"))
    return res


import sphinx.search

sphinx.search.SearchEnglish.split = split
del split

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
    # this is needed by read the docs theme
    "sphinxcontrib.jquery",
]

try:
    import rst2pdf.pdfbuilder
    extensions.append("rst2pdf.pdfbuilder")
except Exception:
    pass

extlinks = {
    'issue': ('https://github.com/rogerbinns/apsw/issues/%s', 'APSW issue %s'),
    'source': ('https://github.com/rogerbinns/apsw/blob/master/%s', '%s'),
}

intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

pygments_style = 'sphinx'

# General substitutions.
project = 'APSW'
author = "Roger Binns <rogerb@rogerbinns.com>"
copyright = f'2004-2023, { author }'
html_logo = "apswlogo.png"

# The default replacements for |version| and |release|, also used in various
# other places throughout the built documents.
#
# The short X.Y version.
version = os.getenv("VERSION")
# The full version, including alpha/beta/rc tags.
release = version
today = os.getenv("RELEASEDATE")
assert version and today

today_fmt = '%B %d, %Y'

exclude_trees = ['build']

add_module_names = False
extlinks_detect_hardcoded_links = True
smartquotes = False

# Options for HTML output

html_title = f"{ project } { version } documentation"
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    "analytics_id": "G-2NR9GDCQLT",
    "style_external_links": True,
    "prev_next_buttons_location": "both",
}

html_favicon = "favicon.ico"

html_static_path = ['.static']
html_last_updated_fmt = '%b %d, %Y'

# One page html
singlehtml_sidebars = {"index": ["globaltoc.html"]}

# epub

epub_basename = f"{ project } { version }"
epub_description = f"Documentation for APSW { version } Python package"
epub_identifier = "https://github.com/rogerbinns/apsw"
epub_scheme = "URL"
epub_cover = (html_logo, "")
viewcode_enable_epub = True
epub_theme = "default"
epub_theme_options = {'nosidebar': True, 'externalrefs': True, 'globaltoc_maxdepth': 1}
epub_show_urls = "no"

# pdf using rst2pdf
pdf_documents = [
    ("index", f"{ project } { version }", html_title, author),
]

pdf_stylesheets = ["sphinx", "a4"]
pdf_fit_mode = "shrink"

# latexpdf
latex_engine = "xelatex"
latex_logo = html_logo

### Extra gunk


def skip_Shell_members(app, what, name, obj, skip, options):
    if name.startswith("command_") or name.startswith("output_"):
        return True
    return skip


def setup(app):
    app.connect('autodoc-skip-member', skip_Shell_members)


nitpicky = True
