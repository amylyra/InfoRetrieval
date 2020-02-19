# -*- coding: utf-8 -*-

"""Sokoglam products spider."""

# Imports =====================================================================

import json
import scrapy

from scrapy.spiders import SitemapSpider
from sokoglam.items import ProductItem, ReviewItem, ReviewerItem
from sokoglam.loaders import ProductItemLoader, ReviewItemLoader, ReviewerItemLoader

# Spider ======================================================================

class SokoglamProductsSpider(SitemapSpider):
    """Sokoglam products spider."""

    name = 'products'
    allowed_domains = ['sokoglam.com', 'yotpo.com']
    sitemap_urls = ['https://sokoglam.com/robots.txt']
    sitemap_rules = [('/products/', 'parse_product')]
    sitemap_follow = ['/sitemap_products']

    # -------------------------------------------------------------------------

    def parse_product(self, response):
        """
        Extract product details.

        @url https://sokoglam.com/products/missha-super-aqua-cell-renew-snail-hydro-gel-mask
        @returns requests 1
        """
        data = response.xpath('//script').re_first('_BISConfig.product = (.+);')
        record = json.loads(data)

        loader = ProductItemLoader(ProductItem(), response)
        loader.add_value('id', record.get('id'))
        loader.add_value('sku', record.get('variants', [{}])[0].get('sku'))
        loader.add_value('name', record.get('title'))
        loader.add_value('brand', record.get('vendor'))
        loader.add_value('handle', record.get('handle'))
        loader.add_value('type', record.get('type'))
        loader.add_value('tags', record.get('tags'))
        loader.add_xpath('category', '//nav[@class="breadcrumb"]/*[not(@class)]')
        loader.add_xpath('staff_review', '//div[@id="staff-review"]/p')
        loader.add_xpath('price_currency', '//meta[@itemprop="priceCurrency"]/@content')
        loader.add_value('price', record.get('price'))
        loader.add_value('price_min', record.get('price_min'))
        loader.add_value('price_max', record.get('price_max'))
        loader.add_value('barcode', record.get('variants', [{}])[0].get('barcode'))
        loader.add_value('inventory_quantity', record.get('variants', [{}])[0].get('inventory_quantity'))
        loader.add_value('featured_image', record.get('featured_image'))
        loader.add_value('images', record.get('images'))
        loader.add_xpath('video', '//div[@id="video"]/iframe/@src')
        loader.add_xpath('how_to', '//div[@id="how-to"]')
        loader.add_css('how_to', '#content3 .tab-content')
        loader.add_xpath('key_ingredients', '//div[@id="key-ingredients"]/p')
        loader.add_css('key_ingredients', '#content2 .pdp-tab-content > p')
        loader.add_xpath('full_ingredients', '//div[@id="full-ingredients"]/p')
        loader.add_css('full_ingredients', '#content2 .tab-content--full > p')
        loader.add_xpath('availability', '//link[@itemprop="availability"]/@href')
        loader.add_value('description', record.get('description'))
        loader.add_value('published_at', record.get('published_at'))
        loader.add_css('rating', '.review-stars .yotpo-stars > .sr-only', re=r'([\d.]+)')
        loader.add_value('url', response.url)
        product = loader.load_item()
        product['reviews'] = []

        appkey = response.xpath('//div[@data-appkey]/@data-appkey').get()
        return self.build_reviews_request(product, appkey)

    # -------------------------------------------------------------------------

    def parse_reviews(self, response):
        """Extract reviews data."""
        product = response.meta.get('product') or ProductItem()

        data = json.loads(response.body)
        content = scrapy.Selector(text=data[0]['result'])
        reviews = content.xpath('//div[@data-review-id != "0"]')
        print(response.meta.get('page', 1) + 1)

        for each in reviews:
            review = self.extract_review(each)
            review['reviewer'] = self.extract_reviewer(each)
            product['reviews'].append(review)
            
        return product if not reviews else self.build_reviews_request(
            product=product,
            appkey=response.meta['appkey'],
            page=response.meta.get('page', 1) + 1
        )

    # -------------------------------------------------------------------------

    def extract_review(self, selector):
        """Extract review details."""
        loader = ReviewItemLoader(ReviewItem(), selector=selector)
        loader.add_css('title', '.content-title')
        loader.add_css('description', '.content-review')
        loader.add_css('rating', '.yotpo-review-stars .sr-only', re=r'([\d.]+)')
        loader.add_css('upvotes', 'span[data-type="up"]')
        loader.add_css('downvotes', 'span[data-type="down"]')
        loader.add_css('date_published', '.yotpo-review-date')
        return loader.load_item()

    # -------------------------------------------------------------------------

    def extract_reviewer(self, selector):
        """Extract reviewer details."""
        loader = ReviewerItemLoader(ReviewerItem(), selector=selector)
        loader.add_css('name', '.yotpo-user-name')
        loader.add_xpath('age', './/span[has-class("yotpo-user-field-description") and contains(., "Age:")]/following-sibling::span')
        loader.add_xpath('skin_type', './/span[has-class("yotpo-user-field-description") and contains(., "Skin Type:")]/following-sibling::span')
        loader.add_css('verified_buyer', '.yotpo-user-title')
        return loader.load_item()

    # -------------------------------------------------------------------------

    def build_reviews_request(self, product, appkey, page=1):
        """Build review request using pid and appkey."""
        data = {
            'methods': json.dumps([
                {
                    'method': 'reviews',
                    'params': {
                        'page': page,
                        'host-widget': 'main_widget',
                        'pid': product['id']
                    }
                }
            ]),
            'app_key': appkey,
            'is_mobile': 'false',
            'widget_version': '2020-02-02_13-52-47'
        }
        return scrapy.FormRequest(
            url='https://staticw2.yotpo.com/batch',
            formdata=data,
            callback=self.parse_reviews,
            meta={
                'page': page,
                'appkey': appkey,
                'product': product
            },
            dont_filter=True
        )

# END =========================================================================
