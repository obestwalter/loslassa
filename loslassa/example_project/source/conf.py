# -*- coding: utf-8 -*-
import sphinx_bootstrap_theme

_my_website_name = "Loslassa Example Page"

# noinspection PyShadowingBuiltins
copyright = '2013, Loslassa Project'
html_title = _my_website_name
html_short_title = "Loslassa"

###############################################################################
language = "en"
extensions = []
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = _my_website_name
#html_theme_options = {}
keep_warnings = True

html_theme = 'bootstrap' # 'haiku'
#html_theme_path = []
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

# (Optional) Logo. Should be exactly 24x24 px to fit the nav. bar.
# Path should be relative to the static files directory.
html_logo = "logo.png"

if html_theme == "bootstrap":
    html_theme_options = {
        # Navigation bar title. (Default: ``project`` value)
        'navbar_title': _my_website_name,
        # Global TOC depth for "site" navbar tab. (Default: 1)
        # Switching to -1 shows all levels.
        'globaltoc_depth': 2,

        # Include hidden TOCs in Site navbar?
        #
        # Note: If this is "false", you cannot have mixed ``:hidden:`` and
        # non-hidden ``toctree`` directives in the same page, or else the build
        # will break.
        #
        # Values: "true" (default) or "false"
        'globaltoc_includehidden': "true",

        # HTML navbar class (Default: "navbar") to attach to <div> element.
        # For black navbar, do "navbar navbar-inverse"
        'navbar_class': "navbar navbar-inverse",

        # Fix navigation bar to top of page?
        # Values: "true" (default) or "false"
        'navbar_fixed_top': "true",

        # Location of link to source.
        # Options are "nav" (default), "footer" or anything else to exclude.
        'source_link_position': "footer",

        # Bootswatch (http://bootswatch.com/) theme.
        #
        # Options are nothing with "" (default) or the name of a valid theme
        # such as "amelia" or "cosmo".
        #
        # Note that this is served off CDN, so won't be available offline.
        'bootswatch_theme': "amelia",
    }

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
#html_last_updated_fmt = '%b %d, %Y'
html_use_smartypants = True
# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

html_domain_indices = False
html_use_index = False
html_show_sourcelink = True
html_show_sphinx = True
html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None
