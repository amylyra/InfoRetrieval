# -*- coding: utf-8 -*-

"""Items"""

# Imports =====================================================================

from scrapy import Item, Field

# Items =======================================================================

class BaseItem(Item):
    """Base item"""

    # -------------------------------------------------------------------------

    def __init__(self, *args, **kwargs):
        super(BaseItem, self).__init__(*args, **kwargs)

        # Set fields default value
        for field_name, meta in self.fields.items():
            if not self.get(field_name):
                self._values[field_name] = meta.get('default', None)

# -----------------------------------------------------------------------------

class ProductItem(BaseItem):
    """Product item"""
    id = Field()
    sku = Field()
    name = Field()
    brand_id = Field()
    brand_name = Field()
    brand_logo_url = Field()
    brand_description = Field()
    brand_url = Field()
    category_name = Field()
    category_url = Field()
    short_description = Field()
    long_description = Field()
    suggested_usage = Field()
    loves_count = Field()
    url = Field()
    variations = Field()
    reviews = Field()
    star_reviews_counts = Field()

# -----------------------------------------------------------------------------

class ProductVariationItem(BaseItem):
    """Product variation item"""
    sku_id = Field()
    sku_name = Field()
    list_price = Field()
    variation_type = Field()
    variation_value = Field()
    thumbnail_url = Field()
    url = Field()

# -----------------------------------------------------------------------------

class ReviewItem(BaseItem):
    """Review item"""
    title = Field()
    quickTake = Field()
    description = Field()
    rating = Field()
    publishedAt = Field()
    reviewer = Field()

# -----------------------------------------------------------------------------

class ReviewerItem(BaseItem):
    """Reviewer item"""
    name = Field()
    skinType = Field()
    skinTone = Field()
    age = Field()
    location = Field()
    eyeColor = Field()
    badge = Field()

# END =========================================================================
