# -*- coding: utf-8 -*-

"""Walgreens Products Spider"""

# Imports =====================================================================

import json

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.url import add_or_replace_parameter, url_query_parameter

from walgreens.items import (
    ProductItem, ReviewItem, ReviewerItem
)
from walgreens.loaders import (
    ProductItemLoader, ReviewItemLoader, ReviewerItemLoader
)

# Spider ======================================================================

class WalgreensProductsSpider(CrawlSpider):
    """Walgreens Products Spider"""

    name = 'products'
    allowed_domains = ['walgreens.com', 'bazaarvoice.com']
    start_urls = ['https://www.walgreens.com/store/catalog/shopLanding']
    rules = (
        Rule(
            LinkExtractor(allow=('/store/c/',), deny=('/ID=[^-]+-product',)),
            callback='parse_listing',
            follow=True
        ),
        Rule(
            LinkExtractor(allow=('/ID=[^-]+-product',)),
            callback='parse_product'
        ),
    )

    # -------------------------------------------------------------------------

    def parse_listing(self, response):
        """Extract product list"""
        blob = response.css('script').re_first(r'__APP_INITIAL_STATE__ = (\{.+\});')
        if not blob:
            return
            
        data = json.loads(blob)

        if not data['searchResult'].get('productList'):
            return

        for each in data['searchResult']['productList']:
            yield response.follow(
                each['productInfo']['productURL'],
                callback=self.parse_product
            )

        limit = response.meta.get('limit', 24)
        offset = int(url_query_parameter(response.url, 'No', 0)) + limit

        yield response.follow(
            add_or_replace_parameter(response.url, 'No', offset),
            callback=self.parse_listing,
            meta={'offset': offset, 'limit': limit}
        )

    # -------------------------------------------------------------------------

    def parse_product(self, response):
        """Extract product details"""
        loader = ProductItemLoader(ProductItem(), response)
        loader.add_value('id', response.url, re=r'/ID=([^-]+)')
        loader.add_css('name', '#productTitle')
        loader.add_css('regular_price', '#regular-price-info')
        loader.add_css('unit_price', '#unit-price')
        loader.add_xpath('category', '//ul[has-class("nav__bread-crumbs")]/li[position() > 2]//a')
        loader.add_value('url', response.url)
        loader.add_css('description', '#Details-0 + .wag-accordion-tab-content[id]')
        loader.add_css('warnings', '#Warnings-1 + .wag-accordion-tab-content[id]')
        loader.add_css('ingredients', '#Ingredients-2 + .wag-accordion-tab-content[id]')
        loader.add_css('shipping', '#Shipping-3 + .wag-accordion-tab-content[id]')
        loader.add_css('main_image', '#productImg::attr(src)')
        loader.add_css('image_urls', '#thumbnailImages img::attr(src)')
        loader.add_css('rating', '#reviewsData > .pr10::text')
        loader.add_css('reviews_count', '#reviewsData > .ml10::text', re=r'\d+')
        product = loader.load_item()

        if product.get('reviews_count') and product['reviews_count'] > 0:
            return self.request_reviews(product)
        return product

    # -------------------------------------------------------------------------

    def parse_reviews(self, response):
        """Extract product reviews"""
        product = response.meta.get('product') or {}
        product['reviews'] = product.get('reviews') or []
        data = json.loads(response.body)

        for each in data['Results']:
            review = self.extract_review(each)
            product['reviews'].append(review)

        if product.get('reviews_count') > len(product['reviews']):
            offset = response.meta.get('offset') + len(data['Results'])
            return self.request_reviews(product, offset=offset)
        return product

    # -------------------------------------------------------------------------

    def request_reviews(self, product, offset=0, limit=30):
        """Request reviews"""
        return scrapy.FormRequest(
            method='GET',
            url='https://api.bazaarvoice.com/data/reviews.json',
            formdata={
                'Filter': 'ProductId:%s' % product['id'],
                'Sort': 'Helpfulness:desc',
                'Limit': str(limit),
                'Offset': str(offset),
                'Include': 'Comments',
                'Stats': 'Reviews',
                'passkey': 'tpcm2y0z48bicyt0z3et5n2xf',
                'apiversion': '5.4'
            },
            meta={'offset': offset, 'limit': limit, 'product': product},
            callback=self.parse_reviews
        )

    # -------------------------------------------------------------------------

    def extract_review(self, data):
        """Extract review details"""
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
        """Extract reviewer details"""
        loader = ReviewerItemLoader(ReviewerItem())
        loader.add_value('id', data.get('AuthorId'))
        loader.add_value('username', data.get('UserNickname'))
        loader.add_value('location', data.get('UserLocation'))
        loader.add_value('properties', {name: data.get('Value') for name, data in data.get('ContextDataValues', {}).items()})
        return loader.load_item()

# END =========================================================================
