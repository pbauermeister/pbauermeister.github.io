AUTHOR = 'Pascal Bauermeister'
SITENAME = 'Programmatically speaking'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Zurich'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
_LINKS = (('Pelican', 'https://getpelican.com/'),
         ('Python.org', 'https://www.python.org/'),
         ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
_SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# Theme
#THEME = 'notmyidea'
THEME = 'pelican-clean-blog'
THEME = 'pelican-bootstrap3'   # issue
#THEME = 'aboutwilson'         # has disqus

# Themes with disqus:
THEME = 'aboutwilson'       # ugly w/o customization
THEME = 'attila'            # not for me
THEME = 'bluegrasshopper'   # not for me
THEME = 'blue-penguin-dark' # not for me
THEME = 'blue-penguin'      # not for me
THEME = 'bold'
THEME = 'bootstrap2-dark'   # not for me
THEME = 'bootstrap2'
THEME = 'bootstrap'         # 3
THEME = 'built-texts'       # needs config
THEME = 'bulrush'           # no
THEME = 'cebong'            # no
THEME = 'chameleon'         # bug
THEME = 'chunk'             # no
THEME = 'cid'               # 2
THEME = 'elegant'           # 2
THEME = 'Flex'              # 1 but MUST adjust /theme/img/profile.png
THEME = 'fresh'
THEME = 'gum'
THEME = 'html5-dopetrope'
THEME = 'hyde'              # 2
THEME = 'iris'              # no
THEME = 'jesuislibre'
THEME = 'lovers'
THEME = 'maggner-pelican'   # bug
THEME = 'mg'                # 1
THEME = 'MinimalXY'
THEME = 'mnmlist'
THEME = 'new-bootstrap2'    # 3
THEME = 'nice-blog'         # 2
THEME = 'nikhil-theme'      # 2
THEME = 'niu-x2'            # bug
THEME = 'pelican-cait'      # 2
THEME = 'pelican-twitchy'   # 3
THEME = 'Peli-Kiera'        # 1+
THEME = 'relapse'           # 4
THEME = 'semantic-ui'       # ?
THEME = 'sneakyidea'
THEME = 'SoMA2'
THEME = 'SoMA'              # 5
THEME = 'storm'             # 2+
THEME = 'subtle'            # Nice but not for here
THEME = 'sundown'
THEME = 'tuxlite_tbs'       # 2
THEME = 'w3-personal-blog'  # 4

THEME = 'Peli-Kiera'        # 1+
THEME = 'pelican-clean-blog'


COLOR_SCHEME_CSS = 'monokai.css'
CSS_OVERRIDE = 'custom.css'
FOOTER_INCLUDE = 'pelican-clean-blog-modified-footer.html'
THEME_TEMPLATES_OVERRIDES = ['extra-templates']

DISQUS_SITENAME = 'pbauermeister-blog'

PLUGIN_PATHS = ["pelican-plugins"]
PLUGINS = [
    #"better_codeblock_line_numbering",
    #"disqus_static"
]

#GOOGLE_ANALYTICS = 'G-S8FN37BSDH'

# Code block line numbering:
MD_EXTENSIONS = ['fenced_code',
                 'codehilite(css_class=highlight, linenums=False)']
PLUGINS = ['better_codeblock_line_numbering']
_MARKDOWN = {
  'extension_configs': {
    'markdown.extensions.codehilite': {'css_class': 'highlight', 'linenums': True},
    'markdown.extensions.extra': {},
    'markdown.extensions.meta': {},
  },
  'output_format': 'html5',
}
