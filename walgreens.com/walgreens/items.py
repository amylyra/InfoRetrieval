# -*- coding: utf-8 -*-

"""Items"""

# Imports =====================================================================

from scrapy import Item, Field

# Items =======================================================================

class ProductItem(Item):
    """Product item"""
    id = Field()
    name = Field()
    regular_price = Field()
    unit_price = Field()
    category = Field()
    url = Field()
    description = Field()
    warnings = Field()
    ingredients = Field()
    shipping = Field()
    reviews = Field()
    reviews_count = Field()
    rating = Field()
    star_reviews_counts = Field()
    main_image = Field()
    image_urls = Field()

# -----------------------------------------------------------------------------

class ReviewItem(Item):
    """Review item"""
    id = Field()
    rating = Field()
    title = Field()
    text = Field()
    is_featured = Field()
    positive_feedback_count = Field()
    negative_feedback_count = Field()
    published_at = Field()
    reviewer = Field()

# -----------------------------------------------------------------------------

class ReviewerItem(Item):
    """Reviewer item"""
    id = Field()
    username = Field()
    location = Field()
    properties = Field()

# END =========================================================================
