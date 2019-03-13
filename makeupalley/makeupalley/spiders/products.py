# -*- coding: utf-8 -*-

"""makeupalley.com products spider."""

# Imports =====================================================================

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
            brand = product.xpath('.//td[1]').get()
            category = product.xpath('.//td[3]').get()

            product_link = product.xpath('.//a[contains(@href, "/product/")]/@href').get()
            yield response.follow(
                url=product_link,
                callback=self.parse_product,
                meta={'category': category, 'brand': brand, 'dont_cache': True}
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
        product['reviews'] = product.get('reviews') or []

        reviews_list = response.xpath('//div[@id="reviews-wrapper"]/div[@class="comments"]')
        for each in reviews_list:
            review = self.extract_review(each)
            review['reviewer'] = self.extract_reviewer(each)
            product['reviews'].append(review)
        reviews_count = product.get('reviewCount') or 0

        for page in response.css('.pager a[href]'):
            yield response.follow(
                page,
                callback=self.parse_listing,
                meta={'dont_cache': True}
            )

        if reviews_count > 0:
            # Parse user profiles if any, start with first profile
            profile_link = product['reviews'][0]['reviewer']['profileUrl']
            yield response.follow(
                url=profile_link,
                callback=self.parse_profile,
                meta={'product': product},
                dont_filter=True
            )
        else:
            yield product

    # -------------------------------------------------------------------------

    def parse_profile(self, response):
        """
        Parse user profile.

        @url https://www.makeupalley.com/p~Starhawke
        @returns items 1
        """
        product = response.meta.get('product') or ProductItem()
        review_idx = response.meta.get('review_idx', 0)

        reviewer = self.extract_reviewer_location(response)
        if reviewer.get('location'):
            product['reviews'][review_idx]['reviewer']['location'] = reviewer['location']

        # Parse next profile, if any
        next_review_idx = review_idx + 1
        if next_review_idx < product.get('reviewCount', 0):
            yield response.follow(
                url=product['reviews'][next_review_idx]['reviewer']['profileUrl'],
                callback=self.parse_profile,
                meta={
                    'product': product,
                    'review_idx': next_review_idx
                },
                dont_filter=True
            )
        else:
            # Last profile, yield full product details
            yield product

    # -------------------------------------------------------------------------

    def extract_product(self, response):
        """Extract product details."""
        loader = ProductItemLoader(ProductItem(), response)
        loader.add_xpath('id', '//div[@id="ItemId"]')
        loader.add_xpath('name', '//div[@id="ProductName"]')
        loader.add_value('brand', response.meta.get('brand'))
        loader.add_value('category', response.meta.get('category'))
        loader.add_xpath('price', '//div[contains(@class, "product-review-stats")]/div/p[@class="price"]', re='Price:(.+)')
        loader.add_xpath('packageQuality', '//div[contains(@class, "product-review-stats")]/div/p[@class="pack"]', re='([0-9.]+)')
        loader.add_xpath('repurchasePercentage', '//div[contains(@class, "product-review-stats")]/div/p[not(span)]', re='([0-9]+)')
        loader.add_xpath('reviewCount', '//div[contains(@class, "product-review-stats")]/div/p/span')
        loader.add_xpath('rating', '//div[contains(@class, "product-review-stats")]/div/h3')
        loader.add_xpath('image', '//div[contains(@class, "product-image")]//img/@src')
        loader.add_xpath('ingredients', '//div[@id="ingredientsContent"]')
        loader.add_value('url', response.url)
        return loader.load_item()

    # -------------------------------------------------------------------------

    def extract_review(self, selector):
        """Extract review details."""
        loader = ReviewItemLoader(ReviewItem(), selector)
        loader.add_xpath('content', './/p[@class="break-word"]')
        loader.add_xpath('rating', './/div[@class="lipies"]/span/@class', re="l-([0-9]+)-0")
        loader.add_xpath('publishedAt', './/div[@class="date"]/p/text()[last()]')
        loader.add_xpath('upvotes', './/div[@class="thumbs"]/p', re='([0-9]+) of')
        loader.add_xpath('totalVotes', './/div[@class="thumbs"]/p', re='[0-9]+ of ([0-9]+)')
        return loader.load_item()

    # -------------------------------------------------------------------------

    def extract_reviewer(self, selector):
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

    def extract_reviewer_location(self, selector):
        """Extract reviewer location."""
        loader = ReviewerItemLoader(ReviewerItem(), selector)
        loader.add_xpath('location', '//div[contains(@class, "details")]/p/b[contains(., "Location")]/following-sibling::text()')
        return loader.load_item()

# END =========================================================================
