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
    gtin = scrapy.Field()
    name = scrapy.Field()
    brandLogo = scrapy.Field()
    brand = scrapy.Field()
    description = scrapy.Field()
    priceCurrency = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()
    category = scrapy.Field()
    reviewCount = scrapy.Field()
    rating = scrapy.Field()
    ingredients = scrapy.Field()
    availability = scrapy.Field()
    shipping = scrapy.Field()
    returnPolicy = scrapy.Field()
    url = scrapy.Field()
    reviews = scrapy.Field()
    starReviewsCounts = scrapy.Field()

# -----------------------------------------------------------------------------

class ReviewItem(BaseItem):
    """Review item"""
    title = scrapy.Field()
    description = scrapy.Field()
    rating = scrapy.Field()
    helpfulCount = scrapy.Field()
    reviewImage = scrapy.Field()
    datePublished = scrapy.Field()
    reviewer = scrapy.Field()

# -----------------------------------------------------------------------------

class ReviewerItem(BaseItem):
    """Reviewer item"""
    name = scrapy.Field()
    profileUrl = scrapy.Field()

# END =========================================================================
