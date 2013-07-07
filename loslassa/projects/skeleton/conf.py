# -*- coding: utf-8 -*-

# Replace the text between the quotes with your settings
_my_website_name = "Loslassa Skeleton Page"
_my_short_title = "Loslassa Skeleton"
_my_copyright_message = "2013, Loslassa Project"

# Replace the theme name between the quotes with one of the themes from below
_my_theme = "bootstrap"

############# AVAILABLE THEMES - DON'T CHANGE ANYTHING BELOW HERE #############

# possible values for _my_theme
bootstrap_themes = [
    "bootstrap", "amelia", "cerulean", "cosmo", "cyborg",
    "journal", "readable", "simplex", "slate", "spacelab",
    "spruce", "superhero", "united"]
# check them out here: http://bootswatch.com/

sphinx_themes = [
    "default", "sphinxdoc", "scrolls", "agogo", "nature", "pyramid",
    "haiku", "traditional", "epub"]
# check them out here http://sphinx-doc.org/theming.html#builtin-themes

###############################################################################
################### You can ignore everything below here ######################
###############################################################################

html_short_title = _my_short_title
html_title = _my_website_name
# noinspection PyShadowingBuiltins
copyright = _my_website_name
language = "en"
extensions = []
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = _my_website_name
keep_warnings = True
html_static_path = ['_static']
#html_last_updated_fmt = '%b %d, %Y'
html_use_smartypants = True
html_domain_indices = False
html_use_index = False
html_show_sourcelink = True
html_show_sphinx = True
html_show_copyright = True
html_theme = _my_theme

if _my_theme == "haiku":
    html_theme_options = {}
    html_theme_path = []

elif _my_theme in bootstrap_themes:
    import sphinx_bootstrap_theme

    # (Optional) Logo. Should be exactly 24x24 px to fit the nav. bar.
    # Path should be relative to the static files directory.
    html_logo = "logo.png"
    html_theme = 'bootstrap'  # 'haiku'
    html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
    html_theme_options = {
        'navbar_title': _my_website_name,
        'globaltoc_depth': 2,
        # Note: If this is "false", you cannot have mixed ``:hidden:`` and
        # Values: "true" (default) or "false"
        'globaltoc_includehidden': "true",
        # "navbar" or "navbar navbar-inverse"
        'navbar_class': "navbar",
        # Values: "true" (default) or "false"
        'navbar_fixed_top': "true",
        # "nav" or, "footer" or anything else to exclude.
        'source_link_position': "footer",
        # Bootswatch (http://bootswatch.com/) theme.
        # Options are nothing with "" (default) or the name of a valid theme
        # such as "amelia" or "cosmo".
        # Note that this is served off CDN, so won't be available offline.
        'bootswatch_theme': _my_theme,
    }
