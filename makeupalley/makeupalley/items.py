# -*- coding: utf-8 -*-

"""Items"""

# Imports =====================================================================

import scrapy

# Items =======================================================================

class BaseItem(scrapy.Item):
    """Base item"""
    def __init__(self, *args, **kwargs):
        super(BaseItem, self).__init__(*args, **kwargs)

        # Set fields default value to None
        for field, meta in self.fields.items():
            if not self.get(field, None):
                self._values[field] = meta.get('default', None)

# -----------------------------------------------------------------------------

class ProductItem(BaseItem):
    """Product item"""
    id = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    image = scrapy.Field()
    category = scrapy.Field()
    price = scrapy.Field()
    packageQuality = scrapy.Field()
    repurchasePercentage = scrapy.Field()
    reviewCount = scrapy.Field()
    rating = scrapy.Field()
    ingredients = scrapy.Field()
    url = scrapy.Field()
    reviews = scrapy.Field()
    starReviewsCounts = scrapy.Field()

# -----------------------------------------------------------------------------

class ReviewItem(BaseItem):
    """Review item"""
    content = scrapy.Field()
    rating = scrapy.Field()
    publishedAt = scrapy.Field()
    upvotes = scrapy.Field()
    totalVotes = scrapy.Field()
    reviewer = scrapy.Field()

# -----------------------------------------------------------------------------

class ReviewerItem(BaseItem):
    """Reviewer item"""
    username = scrapy.Field()
    skin = scrapy.Field()
    hair = scrapy.Field()
    eyes = scrapy.Field()
    age = scrapy.Field()
    location = scrapy.Field()
    profileUrl = scrapy.Field()

# END =========================================================================
