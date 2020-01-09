# -*- coding: utf-8 -*-

"""Scrapy settings for sephora project."""

BOT_NAME = 'sephora'

SPIDER_MODULES = ['sephora.spiders']
NEWSPIDER_MODULE = 'sephora.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; rv:71.0) Gecko/20100101 Firefox/71.0'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = .5
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 0

# Cookies
COOKIES_ENABLED = True

# Telnet Console
TELNETCONSOLE_ENABLED = True

# Downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'sephora.middlewares.GeoRetryMiddleware': 555,
}

# Retry configuration
RETRY_ENABLED = True
RETRY_TIMES = 9
RETRY_HTTP_CODES = [400, 403, 408, 421, 429, 500, 502, 503, 504, 522, 524]
RETRY_PRIORITY_ADJUST = -4

GEO_RETRY_ENABLED = True
GEO_RETRY_ALLOWED_DOMAINS = ['sephora.com', 'bazaarvoice.com']

# Default request headers
DEFAULT_REQUEST_HEADERS = {
    'Accept-Language': 'en-US,en',
}

# Enable and configure the AutoThrottle extension
AUTOTHROTTLE_ENABLED = False
# The initial download delay
AUTOTHROTTLE_START_DELAY = 1
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 5
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 7 * 24 * 60 * 60
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_POLICY = 'scrapy.extensions.httpcache.RFC2616Policy'
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
