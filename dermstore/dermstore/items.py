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
    name = scrapy.Field()
    brand = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()
    category = scrapy.Field()
    customersPurchased = scrapy.Field()
    reviewCount = scrapy.Field()
    ratingValue = scrapy.Field()
    starReviewsCounts = scrapy.Field()
    atGlance = scrapy.Field()
    details = scrapy.Field()
    ingredients = scrapy.Field()
    url = scrapy.Field()
    reviews = scrapy.Field()
    
# -----------------------------------------------------------------------------

class ReviewItem(BaseItem):
    """Review item"""
    title = scrapy.Field()
    description = scrapy.Field()
    rating = scrapy.Field()
    reviewer = scrapy.Field()
    
# -----------------------------------------------------------------------------

class ReviewerItem(BaseItem):
    """Reviewer item"""
    gender = scrapy.Field()
    skinType = scrapy.Field()
    skinTone = scrapy.Field()
    age = scrapy.Field()
    location = scrapy.Field()
    reviewDate = scrapy.Field()
    isVerifiedPurchaser = scrapy.Field()
    
# END =========================================================================
