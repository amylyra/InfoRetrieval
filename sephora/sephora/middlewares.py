# -*- coding: utf-8 -*-

"""Middlewares."""

# Imports =====================================================================

import tldextract
from scrapy.exceptions import NotConfigured

# =============================================================================

class GeoRetryMiddleware:
    """Geo retry middleware."""

    # -------------------------------------------------------------------------

    def __init__(self, settings):
        """Initialize middleware."""
        if not settings.getbool('GEO_RETRY_ENABLED'):
            raise NotConfigured
        self.geo_retry_allowed_domains = settings.getlist('GEO_RETRY_ALLOWED_DOMAINS')
        if not self.geo_retry_allowed_domains:
            raise NotConfigured

    # -------------------------------------------------------------------------

    @classmethod
    def from_crawler(cls, crawler):
        """Instantiate middleware."""
        return cls(crawler.settings)

    def process_response(self, request, response, spider):
        """Retry request if needed."""
        if request.meta.get('dont_geo_retry', False):
            return response
        redirect_urls = request.meta.get('redirect_urls')
        domain = tldextract.extract(response.url).registered_domain.lower()
        if redirect_urls and domain not in self.geo_retry_allowed_domains:
            retryreq = request.replace(url=redirect_urls[0])
            retryreq.dont_filter = True
            return retryreq
        return response

# END =========================================================================
