# -*- coding: utf-8 -*-

AUTHOR = u'Aquiles Carattino'
SITENAME = u'Python For The Lab'
SITEURL = u'https://www.pythonforthelab.com'
TIMEZONE = 'Europe/Amsterdam'
GITHUB_URL = 'https://github.com/PFTL'
PDF_GENERATOR = False

TEMPLATE_PAGES = {'static_index.html': 'index.html',
                 'search.html': 'search/index.html',
                  'static_books.html': 'books/index.html',}

STATIC_PATHS = ['images', 'static', 'pages']

ARTICLE_URL = 'blog/{slug}'
ARTICLE_SAVE_AS = 'blog/{slug}/index.html'

SITEMAP_SAVE_AS = 'sitemap.xml'
FEED_DOMAIN = 'https://www.pythonforthelab.com'

FEED_RSS = 'feed'

MARKUP = ('rst', 'markdown',)

RELATIVE_URLS = True

INDEX_SAVE_AS = 'blog/index.html'

PLUGIN_PATHS = ['plugins',]
PLUGINS = ['new_pigment', 'header_image', 'tipue_search']

LOCALE = 'en_US.utf8'

# Where to store the images
HEADERS_FOLDER = 'static/img'
# Force to re-generate the images even if they exist
FORCE_IMG_REBUILD = False
# Default image header for when one is missing
DEFAULT_HEADER = 'static/img/compartments.jpg'

DEFAULT_PAGINATION = 12