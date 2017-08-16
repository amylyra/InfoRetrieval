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
    barcode = scrapy.Field()
    name = scrapy.Field()
    type = scrapy.Field()
    brand = scrapy.Field()
    description = scrapy.Field()
    tags = scrapy.Field()
    handle = scrapy.Field()
    priceCurrency = scrapy.Field()
    price = scrapy.Field()
    featuredImage = scrapy.Field()
    images = scrapy.Field()
    video = scrapy.Field()
    howTo = scrapy.Field()
    staffReview = scrapy.Field()
    category = scrapy.Field()
    reviewCount = scrapy.Field()
    rating = scrapy.Field()
    keyIngredients = scrapy.Field()
    fullIngredients = scrapy.Field()
    availability = scrapy.Field()
    inventoryQuantity = scrapy.Field()
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
    upvotes = scrapy.Field()
    downvotes = scrapy.Field()
    reviewer = scrapy.Field()

# -----------------------------------------------------------------------------

class ReviewerItem(BaseItem):
    """Reviewer item"""
    name = scrapy.Field()
    age = scrapy.Field()
    skinType = scrapy.Field()
    verifiedBuyer = scrapy.Field()

# END =========================================================================
