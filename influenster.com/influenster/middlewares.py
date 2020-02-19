# -*- coding: utf-8 -*-

"""Middlewares."""

# Imports =====================================================================

from scrapy.item import BaseItem
from scrapy.exceptions import NotConfigured

# =============================================================================

"""This module contains the ``CloudFlareMiddleware``"""

from cfscrape import get_tokens

import logging


class CloudFlareMiddleware:
    """Scrapy middleware to bypass the CloudFlare's anti-bot protection"""

    @staticmethod
    def is_cloudflare_challenge(response):
        """Test if the given response contains the cloudflare's anti-bot protection"""
        
        return (
            response.status in (403, 503)
            and response.headers.get('Server', '').startswith(b'cloudflare')
            and 'captcha-bypass' in response.text
        )

    def process_response(self, request, response, spider):
        """Handle the a Scrapy response"""

        if not self.is_cloudflare_challenge(response):
            return response

        logger = logging.getLogger('cloudflaremiddleware')

        logger.debug(
            'Cloudflare protection detected on %s, trying to bypass...',
            response.url
        )

        cloudflare_tokens, __ = get_tokens(
            request.url,
            user_agent=spider.settings.get('USER_AGENT')
        )

        logger.debug(
            'Successfully bypassed the protection for %s, re-scheduling the request',
            response.url
        )

        request.cookies.update(cloudflare_tokens)
        request.priority = 99999

        return request

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
