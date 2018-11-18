# -*- coding: utf-8 -*-

"""items"""

# Imports =====================================================================

from scrapy import Item, Field

# Items =======================================================================

class ProductItem(Item):
    """Product item"""
    title = Field()
    brand = Field()
    category = Field()
    description = Field()
    image_urls = Field()
    url = Field()
    rating = Field()
    reviews = Field()
    review_count = Field()
    star_reviews_counts = Field()

# -----------------------------------------------------------------------------

class ReviewItem(Item):
    """Review item"""
    body = Field()
    rating = Field()
    reviewer = Field()
    published_at = Field()

# -----------------------------------------------------------------------------

class ReviewerItem(Item):
    """Reviewer item"""
    name = Field()
    avatar_url = Field()
    profile_url = Field()
    location = Field()
    reviews_count = Field()
    badge = Field()
    skin_tone = Field()
    skin_type = Field()
    skin_concerns = Field()
    eyes = Field()

# END =========================================================================
