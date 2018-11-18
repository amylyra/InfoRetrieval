# -*- coding: utf-8 -*-

"""Middlewares"""

# Imports =====================================================================

from scrapy.item import BaseItem
from scrapy.exceptions import NotConfigured

# =============================================================================

class AbsoluteUrlSpiderMiddleware:
    """
    Applies `response.urljoin` on item fields
    sepcified in `ABSOLUTEURL_FIELDS`
    """

    # -------------------------------------------------------------------------

    def __init__(self, settings):
        """Initialize middleware"""
        if not settings.getbool('ABSOLUTEURL_ENABLED'):
            raise NotConfigured
        self.fields = settings.getlist('ABSOLUTEURL_FIELDS')
        if not self.fields:
            raise NotConfigured

    # -------------------------------------------------------------------------

    @classmethod
    def from_crawler(cls, crawler):
        """Instantiate middleware"""
        return cls(crawler.settings)

    # -------------------------------------------------------------------------

    def process_spider_output(self, response, result, spider):
        """Convert relative urls to absolute urls"""
        for each in result:
            if isinstance(each, (BaseItem, dict)):
                fields = [field for field in self.fields if each.get(field)]
                for field in fields:
                    each[field] = response.urljoin(each[field])
            yield each

# END =========================================================================
