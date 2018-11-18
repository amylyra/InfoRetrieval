# -*- coding: utf-8 -*-

"""influenster.com products spider"""

# Imports =====================================================================

from scrapy.spiders import SitemapSpider

from influenster.items import ProductItem, ReviewItem, ReviewerItem
from influenster.itemloaders import (
    ProductItemLoader, ReviewItemLoader, ReviewerItemLoader
)

# Spider ======================================================================

class ProductsSpider(SitemapSpider):
    """influenster.com products spider"""

    name = 'products'
    allowed_domains = ['influenster.com']
    #sitemap_urls = ['https://www.influenster.com/ugc-sitemap.xml']
    sitemap_urls = ['https://www.influenster.com/sitemap-marketplace_product_review.xml']
    sitemap_rules = [
        ('/reviews/', 'parse_product'),
    ]
    sitemap_follow = ['/sitemap-marketplace_product_review.xml']

    # -------------------------------------------------------------------------

    def parse_product(self, response):
        """
        Extract product details

        @url https://www.influenster.com/reviews/lakme-face-magic-skin-tints-souffle-foundation-natural-shell-free-gifts-free-shipping-by-indian-goodness?review_page=2
        @returns items 1 1
        @scrapes title brand category description image_urls url reviews
        """
        loader = ProductItemLoader(ProductItem(), response)
        loader.add_css('title', '#product .product-details > h1')
        loader.add_css('brand', '#product .product-brand-link')
        loader.add_xpath('category', '//ul[has-class("breadcrumbs-v2")]/li[position() < last() - 1]')
        loader.add_css('description', '[data-modal="product-description"] .product-description')
        loader.add_css('description', '#product .product-description')
        loader.add_css('image_urls', '#product .product-images [itemprop="image"]::attr(src)')
        loader.add_css('image_urls', '#product .product-images .product-image-carousel [data-image-url]::attr(data-image-url)')
        loader.add_css('rating', '#product .product-review-stats [data-stars]::attr(data-stars)')
        loader.add_css('review_count', '#product-reviews [data-reviews-count]::attr(data-reviews-count)')
        loader.add_value('url', response.url)
        product = loader.load_item()

        product['reviews'] = []
        for each in response.css('#product-reviews [itemprop="review"]'):
            review = self.extract_review(each)
            product['reviews'].append(review)

        next_page = response.css('link[rel="next"]::attr(href)')
        if next_page:
            return response.follow(
                next_page.get(),
                callback=self.parse_reviews,
                meta={'product': product}
            )

        return product

    # -------------------------------------------------------------------------

    def parse_reviews(self, response):
        """
        Extract reviews details

        @url https://www.influenster.com/reviews/lakme-face-magic-skin-tints-souffle-foundation-natural-shell-free-gifts-free-shipping-by-indian-goodness?review_page=2
        @returns items 1 1
        @scrapes body rating published_at reviewer
        """
        product = response.meta.get('product') or ProductItem()
        product['reviews'] = product.get('reviews') or []
        for each in response.css('#product-reviews [itemprop="review"]'):
            review = self.extract_review(each)
            product['reviews'].append(review)

        next_page = response.css('link[rel="next"]::attr(href)')
        if next_page:
            return response.follow(
                next_page.get(),
                callback=self.parse_reviews,
                meta={'product': product}
            )

        return product

    # -------------------------------------------------------------------------

    def extract_review(self, selector):
        """Extract review details"""
        loader = ReviewItemLoader(ReviewItem(), selector)
        loader.add_css('body', '[itemprop="reviewBody"]')
        loader.add_css('rating', '[itemprop="ratingValue"]::attr(content)')
        loader.add_css('published_at', '[itemprop="datePublished"]')
        loader.add_css('published_at', '[itemprop="datePublished"]::attr(content)')
        loader.add_value('reviewer', self.extract_reviewer(selector))
        return loader.load_item()

    # -------------------------------------------------------------------------

    def extract_reviewer(self, selector):
        """Extract reviewer details"""
        loader = ReviewerItemLoader(ReviewerItem(), selector)
        loader.add_css('name', '.author-name')
        loader.add_css('location', '.author-location')
        loader.add_css('avatar_url', '.avatar > img::attr(data-lazy-src)')
        loader.add_css('profile_url', '.content-item-author-info > a::attr(href)')
        loader.add_css('reviews_count', '.author-reviews-count', re=r'(?i)(\d+)\s+reviews')
        loader.add_css('badge', '.author-badge-text')
        loader.add_xpath('skin_tone', './/div[has-class("review-author-user-profile")]//label[.="Skin Tone:"]/following-sibling::div/span')
        loader.add_xpath('skin_type', './/div[has-class("review-author-user-profile")]//label[.="Skin Type:"]/following-sibling::div/span')
        loader.add_xpath('skin_concerns', './/div[has-class("review-author-user-profile")]//label[.="Skin Concerns:"]/following-sibling::div/span')
        loader.add_xpath('eyes', './/div[has-class("review-author-user-profile")]//label[.="Eyes:"]/following-sibling::div/span')
        return loader.load_item()

# END =========================================================================
