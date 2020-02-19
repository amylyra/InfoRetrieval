# -*- coding: utf-8 -*-

"""Scrapy settings for influenster project."""

BOT_NAME = 'influenster'

SPIDER_MODULES = ['influenster.spiders']
NEWSPIDER_MODULE = 'influenster.spiders'

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

# Retry configuration
RETRY_ENABLED = True
RETRY_TIMES = 9
RETRY_HTTP_CODES = [400, 403, 408, 421, 429, 500, 502, 503, 504, 522, 524]
RETRY_PRIORITY_ADJUST = -4

# Default request headers
DEFAULT_REQUEST_HEADERS = {
    'Accept-Language': 'en-US,en',
    'Referer': 'https://www.influenster.com/',
    'Cookie': '__cfduid=ddeb7247c9543e595e8c918600016d0851578441671; sessionid_v3=0biq3l788gzhch2qd6bkxvsonkomdkir; visited=False; csrftoken=iTXAllamDNoZ1Oa1k8UqK3ptEuYUMlf9AvGA33B12T3drXTGOrdPV8NnxjWRTyHZ; mp_9cc9b840c981980a421375cf78f07176_mixpanel=%7B%22distinct_id%22%3A%20%2216f8274bc19bb-00f3016d993da8-7b6b1635-fa000-16f8274bc1a8e%22%2C%22%24device_id%22%3A%20%2216f8274bc19bb-00f3016d993da8-7b6b1635-fa000-16f8274bc1a8e%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22Current_page_name%22%3A%20%22%22%2C%22Previous_page%22%3A%20%22%22%2C%22platform%22%3A%20%22web%22%2C%22profile_user_id%22%3A%20null%2C%22__mps%22%3A%20%7B%22%24os%22%3A%20%22Windows%22%2C%22%24browser%22%3A%20%22Firefox%22%2C%22%24browser_version%22%3A%2071%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D%2C%22__mpso%22%3A%20%7B%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpap%22%3A%20%5B%5D%7D'
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
