# -*- coding: utf-8 -*-

"""Sephora Products Spider"""

# Imports =====================================================================

import json

import scrapy
from scrapy.spiders import SitemapSpider

from sephora.items import (
    ProductItem, ProductVariationItem, ReviewItem, ReviewerItem
)
from sephora.loaders import (
    ProductItemLoader, ProductVariationItemLoader,
    ReviewItemLoader, ReviewerItemLoader
)

# Spider ======================================================================

class SephoraProductsSpider(SitemapSpider):
    """Sephora Products Spider"""

    name = 'products'
    allowed_domains = ['sephora.com']
    sitemap_urls = ['http://www.sephora.com/products-sitemap.xml']

    # -------------------------------------------------------------------------

    def parse(self, response):
        """Extract product details"""
        blob = response.css('[data-comp="PageJSON"]::text').get()
        data = json.loads(blob)

        item = self.extract_product(data[6]['props']['currentProduct'])

        loader = ProductItemLoader(item)
        loader.add_value('url', response.url)
        return loader.load_item()

    # -------------------------------------------------------------------------

    def parse_reviews(self, response):
        """Extract product reviews"""
        product = response.meta.get('product') or {}

    # -------------------------------------------------------------------------

    def extract_product(self, data):
        """Extract product details"""
        loader = ProductItemLoader(ProductItem())
        loader.add_value('id', data.get('productId'))
        loader.add_value('sku', data.get('fullSiteProductUrl'), re=r'(?i)skuId=(.+)')
        loader.add_value('name', data.get('displayName'))
        loader.add_value('brand_id', data['brand']['brandId'])
        loader.add_value('brand_name', data['brand']['displayName'])
        loader.add_value('brand_logo_url', data['brand']['logo'])
        loader.add_value('brand_description', data['brand']['longDescription'])
        loader.add_value('brand_url', data['brand']['targetUrl'])
        loader.add_value('category_name', data['parentCategory']['displayName'])
        loader.add_value('category_url', data['parentCategory']['targetUrl'])
        loader.add_value('short_description', data.get('quickLookDescription'))
        loader.add_value('long_description', data.get('longDescription'))
        loader.add_value('suggested_usage', data.get('suggestedUsage'))
        loader.add_value('loves_count', data.get('lovesCount'))

        variations = []
        for each in data['regularChildSkus']:
            variation = self.extract_product_variation(each)
            variations.append(variation)
        loader.add_value('variations', variations)

        return loader.load_item()

    # -------------------------------------------------------------------------

    def extract_product_variation(self, data):
        """Extract product variation"""
        loader = ProductVariationItemLoader(ProductVariationItem())
        loader.add_value('sku_id', data.get('skuId'))
        loader.add_value('sku_name', data.get('skuName'))
        loader.add_value('list_price', data.get('listPrice'))
        loader.add_value('thumbnail_url', data.get('smallImage'))
        loader.add_value('url', data.get('targetUrl'))
        loader.add_value('variation_type', data.get('variationType'))
        loader.add_value('variation_value', data.get('variationValue'))
        return loader.load_item()

    # -------------------------------------------------------------------------

    def extract_review(self, selector):
        """Extract review details"""
        loader = ReviewItemLoader(ReviewItem(), selector)
        loader.add_value('reviewer', self.extract_reviewer(selector))
        return loader.load_item()

    # -------------------------------------------------------------------------

    def extract_reviewer(self, selector):
        """Extract reviewer details"""
        loader = ReviewerItemLoader(ReviewerItem(), selector)
        return loader.load_item()

# END =========================================================================
