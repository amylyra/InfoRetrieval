# -*- coding: utf-8 -*-

"""makeupalley.com products spider."""

# Imports =====================================================================

import json

import scrapy
from scrapy.http import JsonRequest
from scrapy.exceptions import CloseSpider

from makeupalley.items import ProductItem, ReviewItem, ReviewerItem
from makeupalley.loaders import (
    ProductItemLoader, ReviewItemLoader, ReviewerItemLoader
)

# Spider ======================================================================

class MakeupAlleyProductsSpider(scrapy.Spider):
    """makeupalley.com products spider."""

    name = 'products'
    allowed_domains = ['makeupalley.com']

    # -------------------------------------------------------------------------

    @staticmethod
    def login_request(username, password):
        """Build login request."""
        return JsonRequest(
            'https://api.makeupalley.com/api/v1/users/auth/login',
            headers={
                'Referer': 'https://www.makeupalley.com/'
            },
            data={
                'userName': username,
                'password': password,
                'rememberMe': True,
                'fromSavedCookie': False
            },
            meta={'handle_httpstatus_list': [401]}
        )

    # -------------------------------------------------------------------------

    def start_requests(self):
        """Attempt login using credentials provided from settings."""
        username = self.settings.get('MAKEUPALLEY_USERNAME')
        password = self.settings.get('MAKEUPALLEY_PASSWORD')
        return [self.login_request(username, password)]

    # -------------------------------------------------------------------------

    def parse(self, response):
        """Check login and redirect to products page."""
        if response.status == 401:
            data = json.loads(response.text)
            error_message = data['message']
            if error_message:
                raise CloseSpider(error_message)

        return scrapy.Request(
            'http://www.makeupalley.com/product/',
            callback=self.parse_categories
        )

    # -------------------------------------------------------------------------

    def parse_categories(self, response):
        """
        Parse categories and request listing for each category.

        @url http://www.makeupalley.com/product/
        @returns requests 1
        """
        categories = response.xpath('//select[@id="categoryID"]/option[position() > 1]')
        for category in categories:
            category_id = category.attrib['value']

            yield scrapy.FormRequest(
                method='GET',
                url='https://www.makeupalley.com/product/searching?Brand=0&BrandName=&CategoryID=4&q=',
                formdata={
                    'Brand': '0',
                    'BrandName': '',
                    'CategoryID': category_id,
                    'q': '',
                    'SK': 'BRAND',
                    'SO': 'ASC'
                },
                callback=self.parse_listing
            )

    # -------------------------------------------------------------------------

    def parse_listing(self, response):
        """
        Parse listing and follow product links and pagination.

        @url https://www.makeupalley.com/product/searching?Brand=0&BrandName=&CategoryID=4&q=&SK=BRAND&SO=ASC
        @returns requests 1
        """
        product_links = response.css('.product-result-row .details > .item-name[href]')
        for product_link in product_links:
            yield response.follow(
                url=product_link,
                callback=self.parse_product_page
            )

        for page in response.css('.pagination .num > a'):
            page_number = int(page.css('::text').get())
            page_url = '%s&page=%s' % (response.url, page_number)

            yield response.follow(
                url=page_url,
                callback=self.parse_listing
            )

    # -------------------------------------------------------------------------

    def parse_product_page(self, response):
        """
        Parse product details and reviews if any.

        @url https://www.makeupalley.com/product/showreview.asp/ItemId=568/Poppy-Convertible-Color/Stila/Blush
        @returns requests 1
        """
        product = self.extract_product(response)

        product['reviews'] = []
        product_id = product['id']
        review_count = product['review_count']

        if review_count == 0:
            return product

        return response.follow(
            url='https://api.makeupalley.com/api/v1/products/%s/reviews' % product_id,
            callback=self.parse_reviews,
            meta={'product': product, 'page': 1}
        )

    # -------------------------------------------------------------------------

    def parse_reviews(self, response):
        """
        Parse product reviews.

        @url https://api.makeupalley.com/api/v1/products/105841/reviews
        @returns requests 1
        """
        product = response.meta.get('product') or ProductItem()
        page = response.meta.get('page', 1)

        data = json.loads(response.text)

        reviews = data['getRecords']
        if not reviews:
            return product

        if not product.get('reviews'):
            product['reviews'] = []

        for each in reviews:
            review = self.extract_review(each)
            review['reviewer'] = self.extract_reviewer(each)
            product['reviews'].append(review)

        product_id = product.get('id')
        next_page = page + 1

        return response.follow(
            url='https://api.makeupalley.com/api/v1/products/%s/reviews?page=%s' % (product_id, next_page),
            callback=self.parse_reviews,
            meta={'product': product, 'page': next_page}
        )

    # -------------------------------------------------------------------------

    @staticmethod
    def extract_product(response):
        """Extract product details."""
        loader = ProductItemLoader(item=ProductItem(), response=response)
        loader.add_value('id', response.url, re=r'ItemId=([^/]+)')
        loader.add_css('name', '.headline > h1 a::text')
        loader.add_css('brand', '.breadcrumb > .brand > a::text')
        loader.add_css('category', '.breadcrumb > .categ > a::text')
        loader.add_css('package_quality', '.packaging::text')
        loader.add_css('repurchase_percentage', '.buyagain::text', re='([0-9]+)')
        loader.add_css('review_count', '.overall-rating::text', re=r'(\d+) reviews')
        loader.add_css('rating', '.lippie-rating-section .rating-value::text')
        loader.add_css('image', '.primary-image > a > img::attr(src)')
        loader.add_value('url', response.url)
        return loader.load_item()

    # -------------------------------------------------------------------------

    @staticmethod
    def extract_review(data):
        """Extract review details."""
        loader = ReviewItemLoader(item=ReviewItem())
        loader.add_value('id', data.get('reviewId'))
        loader.add_value('content', data.get('review'))
        loader.add_value('rating', data.get('rating'))
        loader.add_value('published_at', data.get('reviewDate'))
        loader.add_value('upvotes', data.get('helpful'))
        loader.add_value('total_votes', data.get('votes'))
        return loader.load_item()

    # -------------------------------------------------------------------------

    @staticmethod
    def extract_reviewer(data):
        """Extract reviewer details."""
        loader = ReviewerItemLoader(item=ReviewerItem())
        loader.add_value('username', data.get('userName'))
        loader.add_value('skin_type', data.get('skinType'))
        loader.add_value('skin_tone', data.get('skinTone'))
        loader.add_value('skin_undertone', data.get('skinUndertone'))
        loader.add_value('hair_color', data.get('hairColor'))
        loader.add_value('hair_type', data.get('hairType'))
        loader.add_value('hair_texture', data.get('hairTexture'))
        loader.add_value('eye_color', data.get('eyeColor'))
        loader.add_value('age_range', data.get('ageRange'))
        loader.add_value('reviews_count', data.get('reviews'))
        return loader.load_item()

# END =========================================================================
