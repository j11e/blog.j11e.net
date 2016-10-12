#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import sys
sys.path.append('.')

############################
# GENERAL CONFIG
############################
AUTHOR = u'JD'
SITENAME = u'j11e'
SITEURL = 'https://blog.j11e.net'
#PAGE_PATHS = ['content/pages/index.html', 'content/pages/other.html']

THEME = './themes/blueidea'

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

ARTICLE_URL = '{category}/{slug}'
ARTICLE_SAVE_AS = '{category}/{slug}.html'
USE_FOLDER_AS_CATEGORY = True

##############################
# PLUGINS CONFIG  
##############################
from plugins import neighbors
from plugins import summary
from plugins import clean_summary
from plugins import sitemap
from plugins import gzip_cache

PLUGINS = [summary, clean_summary, sitemap, neighbors, gzip_cache]

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

SUMMARY_MAX_LENGTH = 300
CLEAN_SUMMARY_MAXIMUM = 2

STATIC_PATHS = ['images', 'pages']
DISPLAY_PAGES_ON_MENU = False

# Feed generation is usually not desired when developing
FEED_RSS = None # 'feed.rss.xml'
FEED_ALL_RSS = None # 'all.rss.xml'
CATEGORY_FEED_RSS = None
FEED_ATOM = 'feed.atom.xml'
FEED_ALL_ATOM = 'all.atom.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Home page', 'https://j11e.net'),
         ('Code stuff', 'https://git.j11e.net/'),
         ('Encrypt all the things!', 'https://j11e.net/gpg.txt'),
         ('Come play chess with me', 'https://fr.lichess.org/@/lazyjaydee'),
         ('<span style="display:none">I\'m cool hire me pls</span>', 'https://j11e.net/cv.pdf'),)

# Social widget
SOCIAL = (('Twitter', 'https://twitter.com/jdinnocenti'),
        ('LinkedIn', 'https://www.linkedin.com/in/jdinnocenti/en'),
        ('GitHub', 'https://www.github.com/j11e'))

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

