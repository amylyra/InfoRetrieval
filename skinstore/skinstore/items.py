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
    brandLogo = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    priceCurrency = scrapy.Field()
    image = scrapy.Field()
    category = scrapy.Field()
    condition = scrapy.Field()
    availability =  scrapy.Field()
    reviewCount = scrapy.Field()
    ratingValue = scrapy.Field()
    starReviewsCounts = scrapy.Field()
    directions = scrapy.Field()
    ingredients = scrapy.Field()
    volume = scrapy.Field()
    range = scrapy.Field()
    size = scrapy.Field()
    url = scrapy.Field()
    reviews = scrapy.Field()
    
# -----------------------------------------------------------------------------

class ReviewItem(BaseItem):
    """Review item"""
    title = scrapy.Field()
    description = scrapy.Field()
    rating = scrapy.Field()
    datePublished = scrapy.Field()
    upVotes = scrapy.Field()
    downVotes = scrapy.Field()
    reviewer = scrapy.Field()
    
# -----------------------------------------------------------------------------

class ReviewerItem(BaseItem):
    """Reviewer item"""
    username = scrapy.Field()
    
# END =========================================================================
