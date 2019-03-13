# -*- coding: utf-8 -*-

"""makeupalley.com products spider."""

# Imports =====================================================================

from functools import partial
from operator import itemgetter
from collections import defaultdict

import scrapy
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

    def __init__(self, *args, **kwargs):
        """Initialize spider."""
        super().__init__(*args, **kwargs)
        self.reviews = defaultdict(partial(defaultdict, dict))
        self.processed_reviews = defaultdict(list)

    # -------------------------------------------------------------------------

    @staticmethod
    def login_request(username, password, callback):
        """Build login request."""
        return scrapy.FormRequest(
            'https://www.makeupalley.com/account/login.asp',
            formdata={
                'sendtourl': 'http://www.makeupalley.com/product/',
                'UserName': username,
                'Password': password,
                'remember': 'on',
            },
            callback=callback,
            meta={'dont_cache': True}
        )

    # -------------------------------------------------------------------------

    def start_requests(self):
        """Attempt login using credentials provided from settings."""
        username = self.settings.get('MAKEUPALLEY_USERNAME')
        password = self.settings.get('MAKEUPALLEY_PASSWORD')
        return [self.login_request(username, password, callback=self.check_login)]

    # -------------------------------------------------------------------------

    def check_login(self, response):
        """Check login and redirect to products page."""
        # Check if login attempt was successful
        error_message = response.css('#LoginMUA > div > .Error::text').get()
        if error_message:
            raise CloseSpider(error_message)

        return scrapy.Request(
            'http://www.makeupalley.com/product/',
            callback=self.parse_categories,
            meta={'dont_cache': True}
        )

    # -------------------------------------------------------------------------

    def parse_categories(self, response):
        """
        Parse categories and request listing for each category.

        @url http://www.makeupalley.com/product/
        @returns requests 1
        """
        categories = response.xpath('//select[@id="CategoryID"]/option[position() > 1]')
        for category in categories:
            category_id = category.attrib['value']
            yield scrapy.FormRequest(
                method='GET',
                url='http://www.makeupalley.com/product/searching.asp',
                formdata={
                    'Brand': '',
                    'BrandName': '',
                    'CategoryID': category_id,
                    'title': ''
                },
                callback=self.parse_listing,
                meta={'dont_cache': True}
            )

    # -------------------------------------------------------------------------

    def parse_listing(self, response):
        """
        Parse listing and follow products link and pagination.

        @url https://www.makeupalley.com/product/searching.asp?Brand=&BrandName=&CategoryID=4&title=
        @returns requests 1
        """
        products = response.xpath('//div[@class="search-results"]/div/table/tr')
        for product in products:
            brand_name = product.xpath('.//td[1]').get()
            category_name = product.xpath('.//td[3]').get()

            product_link = product.xpath('.//a[contains(@href, "/product/")]/@href').get()
            yield response.follow(
                url=product_link,
                callback=self.parse_product,
                meta={
                    'category_name': category_name,
                    'brand_name': brand_name,
                    'is_first_page': True,
                    'dont_cache': True
                }
            )

        for page in response.css('.pager a[href]'):
            yield response.follow(
                page,
                callback=self.parse_listing,
                meta={'dont_cache': True}
            )

    # -------------------------------------------------------------------------

    def parse_product(self, response):
        """
        Parse product details.

        @url https://www.makeupalley.com/product/showreview.asp/ItemId=10301/Instant-Cheekbones-Contouring-Blush/COVERGIRL/Blush
        @returns requests 1
        """
        product = response.meta.get('product') or self.extract_product(response)
        is_first_page = response.meta.get('is_first_page')
        product_id = product['id']

        reviews_list = response.xpath('//div[@id="reviews-wrapper"]/div[@class="comments"]')
        if is_first_page and not reviews_list:
            return product

        for each in reviews_list:
            review = self.extract_review(each)
            review['reviewer'] = self.extract_reviewer(each)

            review_id = review['id']
            self.reviews[product_id][review_id] = review

            profile_link = review['reviewer']['profileUrl']
            yield response.follow(
                url=profile_link,
                callback=self.parse_profile,
                meta={
                    'product': product,
                    'review_id': review_id
                },
                dont_filter=True
            )

        for page in response.css('.pager a[href]'):
            yield response.follow(
                page,
                callback=self.parse_product,
                meta={
                    'product': product,
                    'is_first_page': False,
                    'dont_cache': True
                }
            )

    # -------------------------------------------------------------------------

    def parse_profile(self, response):
        """
        Parse user profile.

        @url https://www.makeupalley.com/p~Starhawke
        @returns items 0
        """
        product = response.meta.get('product') or ProductItem()
        review_id = response.meta.get('review_id')
        product_id = product.get('id')
        if product_id is None:
            return

        reviewer = self.extract_reviewer_location(response)
        if reviewer.get('location'):
            self.reviews[product_id][review_id]['reviewer']['location'] = reviewer['location']

        self.processed_reviews[product_id].append(self.reviews[product_id].pop(review_id))

        if len(self.processed_reviews[product_id]) == product['reviewCount']:
            product['reviews'] = sorted(
                self.processed_reviews.pop(product_id),
                key=itemgetter('publishedAt'),
                reverse=True
            )
            del self.reviews[product_id]
            return product

    # -------------------------------------------------------------------------

    @staticmethod
    def extract_product(response):
        """Extract product details."""
        loader = ProductItemLoader(ProductItem(), response)
        loader.add_xpath('id', '//div[@id="ItemId"]')
        loader.add_xpath('name', '//div[@id="ProductName"]')
        loader.add_value('brand', response.meta.get('brand_name'))
        loader.add_value('category', response.meta.get('category_name'))
        loader.add_xpath('price', '//div[has-class("product-review-stats")]/div/p[@class="price"]', re='(?i)Price:(.+)')
        loader.add_xpath('packageQuality', '//div[has-class("product-review-stats")]/div/p[@class="pack"]', re='([0-9.]+)')
        loader.add_xpath('repurchasePercentage', '//div[has-class("product-review-stats")]/div/p[not(span)]', re='([0-9]+)')
        loader.add_xpath('reviewCount', '//div[has-class("product-review-stats")]/div/p/span')
        loader.add_xpath('rating', '//div[has-class("product-review-stats")]/div/h3')
        loader.add_xpath('image', '//div[has-class("product-image")]//img/@src')
        loader.add_xpath('ingredients', '//div[@id="ingredientsContent"]')
        loader.add_value('url', response.url)
        return loader.load_item()

    # -------------------------------------------------------------------------

    @staticmethod
    def extract_review(selector):
        """Extract review details."""
        loader = ReviewItemLoader(ReviewItem(), selector)
        loader.add_xpath('id', './/p[@class="break-word"]/@id')
        loader.add_xpath('content', './/p[@class="break-word"]')
        loader.add_xpath('rating', './/div[@class="lipies"]/span/@class', re='l-([0-9]+)-0')
        loader.add_xpath('publishedAt', './/div[@class="date"]/p/text()[last()]')
        loader.add_xpath('upvotes', './/div[@class="thumbs"]/p', re='(?i)([0-9]+) of')
        loader.add_xpath('totalVotes', './/div[@class="thumbs"]/p', re='(?i)[0-9]+ of ([0-9]+)')
        return loader.load_item()

    # -------------------------------------------------------------------------

    @staticmethod
    def extract_reviewer(selector):
        """Extract reviewer details."""
        loader = ReviewerItemLoader(ReviewerItem(), selector)
        loader.add_xpath('username', './/a[@class="track_User_Profile"]')
        loader.add_xpath('skin', './/div[@class="important"]/p/b[contains(., "Skin")]/following-sibling::text()', re=':(.+)')
        loader.add_xpath('hair', './/div[@class="important"]/p/b[contains(., "Hair")]/following-sibling::text()', re=':(.+)')
        loader.add_xpath('eyes', './/div[@class="important"]/p/b[contains(., "Eyes")]/following-sibling::text()', re=':(.+)')
        loader.add_xpath('age', './/div[@class="important"]/p/b[contains(., "Age")]/following-sibling::text()', re=':(.+)')
        loader.add_xpath('profileUrl', './/a[@class="track_User_Profile"]/@href')
        return loader.load_item()

    # -------------------------------------------------------------------------

    @staticmethod
    def extract_reviewer_location(selector):
        """Extract reviewer location."""
        loader = ReviewerItemLoader(ReviewerItem(), selector)
        loader.add_xpath('location', '//div[has-class("details")]/p/b[contains(., "Location")]/following-sibling::text()')
        return loader.load_item()

# END =========================================================================
