# -*- coding: utf-8 -*-

"""Sephora products spider."""

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
    """Sephora products spider."""

    name = 'products'
    allowed_domains = ['sephora.com', 'api.bazaarvoice.com']
    sitemap_urls = ['http://www.sephora.com/products-sitemap.xml']

    # -------------------------------------------------------------------------

    def parse(self, response):
        """
        Extract product details.

        @url https://www.sephora.com/product/double-ended-blemish-extractor-P0417
        @returns requests 1
        """
        blob = response.css('[data-comp="PageJSON"]::text').get()
        data = json.loads(blob)

        item = self.extract_product(data[3]['props']['currentProduct'])

        loader = ProductItemLoader(item)
        loader.add_value('url', response.url)
        product = loader.load_item()

        if product.get('reviews_count') > 0:
            return self.request_reviews(product)
        return product

    # -------------------------------------------------------------------------

    def parse_reviews(self, response):
        """
        Extract product reviews.

        @url https://api.bazaarvoice.com/data/reviews.json?Filter=ProductId%3AP0417&Sort=SubmissionTime%3Aasc&Limit=30&Offset=0&Include=Comments&Stats=Reviews&passkey=rwbw526r2e7spptqd2qzbkp7&apiversion=5.4&Locale=en_US
        @returns items 1
        """
        product = response.meta.get('product') or {}
        product['reviews'] = product.get('reviews') or []
        data = json.loads(response.body)

        for each in data['Results']:
            review = self.extract_review(each)
            product['reviews'].append(review)

        if product.get('reviews_count', 0) > len(product['reviews']):
            offset = response.meta.get('offset') + len(data['Results'])
            return self.request_reviews(product, offset=offset)
        return product

    # -------------------------------------------------------------------------

    def request_reviews(self, product, offset=0, limit=30):
        """Request reviews."""
        return scrapy.FormRequest(
            method='GET',
            url='https://api.bazaarvoice.com/data/reviews.json',
            formdata={
                'Filter': 'ProductId:%s' % product['id'],
                'Sort': 'SubmissionTime:asc',
                'Limit': str(limit),
                'Offset': str(offset),
                'Include': 'Comments',
                'Stats': 'Reviews',
                'passkey': 'rwbw526r2e7spptqd2qzbkp7',
                'apiversion': '5.4',
                'Locale': 'en_US',
            },
            meta={
                'offset': offset,
                'limit': limit,
                'product': product
            },
            callback=self.parse_reviews
        )

    # -------------------------------------------------------------------------

    def extract_product(self, data):
        """Extract product details."""
        loader = ProductItemLoader(ProductItem())
        loader.add_value('id', data.get('productId'))
        loader.add_value('sku', data.get('fullSiteProductUrl'), re=r'(?i)skuId=([^&]+)')
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
        loader.add_value('ingredients', data['currentSku'].get('ingredientDesc'))
        loader.add_value('image_urls', [url for name, url in data['currentSku'].get('skuImages', {}).items()])
        loader.add_value('list_price', data['currentSku'].get('listPrice'))
        loader.add_value('value_price', data['currentSku'].get('valuePrice'))
        loader.add_value('is_sephora_exclusive', data['currentSku'].get('isSephoraExclusive'))
        loader.add_value('is_new', data['currentSku'].get('isNew'))
        loader.add_value('is_out_of_stock', data['currentSku'].get('isOutOfStock'))
        loader.add_value('loves_count', data.get('lovesCount'))
        loader.add_value('rating', data.get('rating'))
        loader.add_value('reviews_count', data.get('reviews'))

        if data.get('regularChildSkus'):
            variations = []
            for each in data['regularChildSkus']:
                variation = self.extract_product_variation(each)
                variations.append(variation)
            loader.add_value('variations', variations)

        return loader.load_item()

    # -------------------------------------------------------------------------

    def extract_product_variation(self, data):
        """Extract product variation."""
        loader = ProductVariationItemLoader(ProductVariationItem())
        loader.add_value('sku_id', data.get('skuId'))
        loader.add_value('sku_name', data.get('skuName'))
        loader.add_value('list_price', data.get('listPrice'))
        loader.add_value('thumbnail_url', data.get('smallImage'))
        loader.add_value('url', data.get('targetUrl'))
        loader.add_value('variation_type', data.get('variationType'))
        loader.add_value('variation_value', data.get('variationValue'))
        loader.add_value('is_sephora_exclusive', data.get('isSephoraExclusive'))
        loader.add_value('is_new', data.get('isNew'))
        loader.add_value('is_out_of_stock', data.get('isOutOfStock'))
        loader.add_value('image_urls', [url for name, url in data.get('skuImages', {}).items()])
        return loader.load_item()

    # -------------------------------------------------------------------------

    def extract_review(self, data):
        """Extract review details."""
        loader = ReviewItemLoader(ReviewItem())
        loader.add_value('id', data.get('Id'))
        loader.add_value('rating', data.get('Rating'))
        loader.add_value('title', data.get('Title'))
        loader.add_value('text', data.get('ReviewText'))
        loader.add_value('is_featured', data.get('IsFeatured'))
        loader.add_value('published_at', data.get('SubmissionTime'))
        loader.add_value('positive_feedback_count', data.get('TotalPositiveFeedbackCount'))
        loader.add_value('negative_feedback_count', data.get('TotalNegativeFeedbackCount'))
        loader.add_value('reviewer', self.extract_reviewer(data))
        return loader.load_item()

    # -------------------------------------------------------------------------

    def extract_reviewer(self, data):
        """Extract reviewer details."""
        loader = ReviewerItemLoader(ReviewerItem())
        loader.add_value('id', data.get('AuthorId'))
        loader.add_value('username', data.get('UserNickname'))
        loader.add_value('location', data.get('UserLocation'))
        loader.add_value('properties', {name: data.get('Value') for name, data in data.get('ContextDataValues', {}).items()})
        return loader.load_item()

# END =========================================================================
