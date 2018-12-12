# -*- coding: utf-8 -*-

"""realself.com products spider"""

# Imports =====================================================================

from scrapy.spiders import SitemapSpider

from realself.items import (
    TreatmentItem, ReviewItem, ReviewEntryItem,
    ReviewerItem, DoctorReviewItem
)
from realself.itemloaders import (
    TreatmentItemLoader, ReviewItemLoader, ReviewerItemLoader,
    ReviewEntryItemLoader, DoctorReviewItemLoader
)

# Spider ======================================================================

class ReviewsSpider(SitemapSpider):
    """realself.com products spider"""

    name = 'reviews'
    allowed_domains = ['realself.com']
    sitemap_urls = ['https://www.realself.com/XMLSitemap']
    sitemap_rules = [
        ('/review/', 'parse_review'),
    ]
    sitemap_follow = ['/xmlsitemap-Review']

    # -------------------------------------------------------------------------

    def parse_review(self, response):
        """
        Extract review details

        @url https://www.realself.com/review/san-diego-ca-tummy-tuck-46-years-11-years-overdue-finally-tt-w-lipo?offset=0&sle=0
        @returns items 1 1
        @scrapes id title tags helpful_count reviewer url entries treatment doctor_review
        """
        loader = ReviewItemLoader(ReviewItem(), response)
        loader.add_css('id', '[property="rs:content-id"]::attr(content)')
        loader.add_css('title', '#review-view h1')
        loader.add_css('tags', '[name="sailthru.tags"]::attr(content)')
        loader.add_css('helpful_count', '[name="sailthru.vote-count"]::attr(content)')
        loader.add_value('reviewer', self.extract_reviewer(response))
        loader.add_value('url', response.url)
        loader.add_value('entries', self.extract_review_entries(response))
        loader.add_value('treatment', self.extract_treatment(response))
        loader.add_value('doctor_review', self.extract_doctor_review(response))
        return loader.load_item()

    # -------------------------------------------------------------------------

    def extract_review_entries(self, selector):
        """Extract review entries"""
        entries = []
        for each in selector.css('#review-entries .review-entry'):
            entry = self.extract_review_entry(each)
            entries.append(entry)
        return entries

    # -------------------------------------------------------------------------

    def extract_review_entry(self, selector):
        """Extract review entry details"""
        loader = ReviewEntryItemLoader(ReviewEntryItem(), selector)
        loader.add_css('title', '.Content-title')
        loader.add_css('body', '.Content-bodyText')
        loader.add_css('published_at', '.Content-byline > .Byline-item')
        loader.add_css('tags', '.Content-tags > li')
        loader.add_css('helpful_count', '.u-marginMedium::attr(rs-static-data)', re=r'(?i)"likeCount":"(\d+)"')
        loader.add_css('image_urls', '.Content-images .Gallery-image::attr(data-original)')
        return loader.load_item()

    # -------------------------------------------------------------------------

    def extract_reviewer(self, selector):
        """Extract reviewer details"""
        loader = ReviewerItemLoader(ReviewerItem(), selector)
        loader.add_css('id', '[property="rs:author-user-id"]::attr(content)')
        loader.add_css('username', '[property="rs:author-user-name"]::attr(content)')
        loader.add_css('avatar_url', 'img.Byline-itemIcon.Avatar::attr(src)')
        loader.add_css('profile_url', '.Byline-item [popover-content-url]::attr(href)')
        return loader.load_item()

    # -------------------------------------------------------------------------

    def extract_treatment(self, selector):
        """Extract treatment details"""
        loader = TreatmentItemLoader(TreatmentItem(), selector)
        loader.add_css('id', '[property="rs:topic-id"]::attr(content)')
        loader.add_css('name', '[property="rs:topic-name"]::attr(content)')
        loader.add_css('treated_at', '[name="sailthru.treatment-date"]::attr(content)')
        loader.add_css('reported_cost', '[property="rs:reported-cost"]::attr(content)')
        loader.add_css('worth_it', '[property="rs:worth-it"]::attr(content)')
        return loader.load_item()

    # -------------------------------------------------------------------------

    def extract_doctor_review(self, selector):
        """Extract doctor review details"""
        loader = DoctorReviewItemLoader(DoctorReviewItem(), selector)
        loader.add_css('id', '[property="rs:doctor-id"]::attr(content)')
        loader.add_css('name', '[property="rs:doctor-name"]::attr(content)')
        loader.add_css('title', '#dr-review > .Media--providerCard > .Media-body > .BodyText--secondary')
        loader.add_css('location', '[property="rs:doctor-location"]::attr(content)')
        loader.add_css('avatar_url', '#dr-review > .Media--providerCard > .Media-figure .Media-figureImage::attr(data-original)')
        loader.add_css('profile_url', '#dr-review > .Media--providerCard > .Media-figure > a::attr(href)')
        loader.add_css('rating', '[name="sailthru.doctor-rating"]::attr(content)')
        loader.add_css('review', '#dr-review > .BodyText')
        return loader.load_item()

# END =========================================================================
