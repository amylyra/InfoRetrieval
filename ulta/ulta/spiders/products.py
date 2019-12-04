# -*- coding: utf-8 -*-

"""Ulta products spider."""

# Imports =====================================================================

import json

import scrapy
from scrapy.spiders import SitemapSpider
from furl import furl

from ulta.items import ProductItem, ReviewItem, ReviewerItem
from ulta.loaders import ProductItemLoader

# Spider ======================================================================

class UltaProductsSpider(SitemapSpider):
    """Ulta products spider."""

    name = 'products'
    allowed_domains = ['ulta.com', 'powerreviews.com']
    sitemap_urls = ['https://www.ulta.com/robots.txt']
    sitemap_follow = ['/detail[0-9]+.xml']
    sitemap_rules = [('product', 'parse')]

    powerreviews_apikey = 'daa0f241-c242-4483-afb7-4449942d1a2b'

    # -------------------------------------------------------------------------

    def parse(self, response):
        """
        Parse product details.

        @url https://www.ulta.com/automatic-eye-liner?productId=1612
        @returns requests 1 1
        """
        product = self.extract_product(response)
        return self.reviews_request(product)

    # -------------------------------------------------------------------------

    def parse_reviews(self, response):
        """
        Parse product reviews.

        @url https://display.powerreviews.com/m/6406/l/en_US/product/xlsImpprod5020095/reviews?apikey=daa0f241-c242-4483-afb7-4449942d1a2b
        @returns requests 1 1
        """
        product = response.meta.get('product') or ProductItem()
        product['reviews'] = product.get('reviews') or []

        data = json.loads(response.text)

        rollup = data['results'][0].get('rollup')
        if rollup:
            product['rating_histogram'] = {
                stars: count
                for stars, count in enumerate(rollup.get('rating_histogram', []), start=1)
            }
            product['rating'] = rollup.get('average_rating')
            product['review_count'] = rollup.get('review_count')
            product['recommended_ratio'] = rollup.get('recommended_ratio')
            product['faceoff_positive'] = rollup.get('faceoff_positive')
            product['faceoff_negative'] = rollup.get('faceoff_negative')
            product['properties'] = {
                property['name']: {
                    value['label']: value['count']
                    for value in property.get('values', [])[:5]
                }
                for property in rollup.get('properties', {})
            }

        reviews = data['results'][0].get('reviews', [])
        for each in reviews:
            review = self.extract_review(each)
            review['reviewer'] = self.extract_reviewer(each)
            product['reviews'].append(review)

        next_page_url = data['paging'].get('next_page_url')
        if next_page_url:
            next_page_url = furl(next_page_url).add({
                'apikey': self.powerreviews_apikey
            }).url
            return response.follow(
                next_page_url,
                callback=self.parse_reviews,
                meta={'product': product}
            )

        return product

    # -------------------------------------------------------------------------

    def reviews_request(self, product):
        """Return product reviews request."""
        return scrapy.FormRequest(
            method='GET',
            url='https://display.powerreviews.com/m/6406/l/en_US/product/%s/reviews' % product['id'],
            formdata={'apikey': self.powerreviews_apikey},
            callback=self.parse_reviews,
            meta={'product': product}
        )

    # -------------------------------------------------------------------------

    @staticmethod
    def extract_product(response):
        """Extract product details."""
        loader = ProductItemLoader(ProductItem(), response)
        loader.add_value('id', response.url, re=r'(?i)productId=([^&]+)')
        loader.add_css('sku', '.ProductMainSection__itemNumber::attr(data-itemnumber)')
        loader.add_css('name', '.ProductMainSection__productName')
        loader.add_css('brand', '.ProductMainSection__brandName')
        loader.add_css('brand', '[property="og:brand"]::attr(content)')
        loader.add_css('brand_page', '.ProductMainSection__brandName > a::attr(href)')
        loader.add_xpath('category', '//div[@class="Breadcrumb"]/ul/li/a[position() > 1]')
        loader.add_css('short_description', '[property="og:description"]::attr(content)')
        loader.add_css('long_description', '.ProductDetail__productDetails > .ProductDetail__productContent')
        loader.add_xpath('price', '//meta[@property="product:price:amount"]/@content')
        loader.add_xpath('priceCurrency', '//meta[@property="product:price:currency"]/@content')
        loader.add_css('image', '[property="og:image"]::attr(content)')
        loader.add_css('offer_message', '.ProductMainSection__offerMessage')
        loader.add_css('how_to_use', '.ProductDetail__howToUse > .ProductDetail__productContent')
        loader.add_css('ingredients', '.ProductDetail__ingredients > .ProductDetail__productContent')
        loader.add_value('url', response.url)
        return loader.load_item()

    # -------------------------------------------------------------------------

    @staticmethod
    def extract_review(data):
        """Extract review details."""
        properties = {
            property['key']: property['value']
            for property in data['details'].get('properties', [])
        }

        return ReviewItem(
            id=data['review_id'],
            title=data['details'].get('headline'),
            body=data['details'].get('comments'),
            created_at=data['details'].get('created_date'),
            updated_at=data['details'].get('updated_date'),
            bottom_line=data['details'].get('bottom_line'),
            pros=properties.get('pros'),
            cons=properties.get('cons'),
            best_uses=properties.get('bestuses'),
            rating=data['metrics'].get('rating'),
            helpful_votes=data['metrics'].get('helpful_votes'),
            not_helpful_votes=data['metrics'].get('not_helpful_votes'),
            helpful_score=data['metrics'].get('helpful_score')
        )

    # -------------------------------------------------------------------------

    @staticmethod
    def extract_reviewer(data):
        """Extract reviewer details."""
        properties = {
            property['key']: property['value']
            for property in data['details'].get('properties', [])
        }

        reviewer = ReviewerItem(
            nickname=data['details'].get('nickname'),
            location=data['details'].get('location'),
            badges=data.get('badges'),
            properties=properties.get('describeyourself')
        )

        reviewer_age = properties.get('age')
        if reviewer_age:
            reviewer['age'] = reviewer_age

        return reviewer

# END =========================================================================
