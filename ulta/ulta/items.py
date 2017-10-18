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
    sku = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    priceCurrency = scrapy.Field()
    promo = scrapy.Field()
    video = scrapy.Field()
    size = scrapy.Field()
    sizeUOM = scrapy.Field()
    recommendationPercentage = scrapy.Field()
    image = scrapy.Field()
    reviewCount = scrapy.Field()
    rating = scrapy.Field()
    restrictions = scrapy.Field()
    reviewersProfile = scrapy.Field()
    gift = scrapy.Field()
    bestUses = scrapy.Field()
    pros = scrapy.Field()
    cons = scrapy.Field()
    ingredients = scrapy.Field()
    howToUse = scrapy.Field()
    hairType = scrapy.Field()
    beautyRoutine = scrapy.Field()
    url = scrapy.Field()
    reviews = scrapy.Field()
    starReviewsCounts = scrapy.Field()

# -----------------------------------------------------------------------------

class ReviewItem(BaseItem):
    """Review item"""
    title = scrapy.Field()
    description = scrapy.Field()
    rating = scrapy.Field()
    datePublished = scrapy.Field()
    bottomLine = scrapy.Field()
    pros = scrapy.Field()
    cons = scrapy.Field()
    bestUses = scrapy.Field()
    reviewer = scrapy.Field()

# -----------------------------------------------------------------------------

class ReviewerItem(BaseItem):
    """Reviewer item"""
    name = scrapy.Field()
    skinType = scrapy.Field()
    bio = scrapy.Field()
    age = scrapy.Field()
    location = scrapy.Field()

# END =========================================================================
