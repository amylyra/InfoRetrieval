# -*- coding: utf-8 -*-

"""Items."""

# Imports =====================================================================

import scrapy

# Items =======================================================================

class ProductItem(scrapy.Item):
    """Product item."""

    id = scrapy.Field()
    sku = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    brand_page = scrapy.Field()
    category = scrapy.Field()
    short_description = scrapy.Field()
    long_description = scrapy.Field()
    price = scrapy.Field()
    priceCurrency = scrapy.Field()
    offer_message = scrapy.Field()
    image = scrapy.Field()
    bestUses = scrapy.Field()
    ingredients = scrapy.Field()
    how_to_use = scrapy.Field()
    url = scrapy.Field()
    reviews = scrapy.Field()
    review_count = scrapy.Field()
    rating = scrapy.Field()
    rating_histogram = scrapy.Field()
    recommended_ratio = scrapy.Field()
    faceoff_positive = scrapy.Field()
    faceoff_negative = scrapy.Field()
    properties = scrapy.Field()

# -----------------------------------------------------------------------------

class ReviewItem(scrapy.Item):
    """Review item."""

    id = scrapy.Field()
    title = scrapy.Field()
    body = scrapy.Field()
    rating = scrapy.Field()
    bottom_line = scrapy.Field()
    pros = scrapy.Field()
    cons = scrapy.Field()
    best_uses = scrapy.Field()
    reviewer = scrapy.Field()
    created_at = scrapy.Field()
    updated_at = scrapy.Field()
    helpful_votes = scrapy.Field()
    not_helpful_votes = scrapy.Field()
    helpful_score = scrapy.Field()

# -----------------------------------------------------------------------------

class ReviewerItem(scrapy.Item):
    """Reviewer item."""

    nickname = scrapy.Field()
    location = scrapy.Field()
    age = scrapy.Field()
    badges = scrapy.Field()
    properties = scrapy.Field()

# END =========================================================================
