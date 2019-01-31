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
    ingredients = Field()
    loves_count = Field()
    url = Field()
    variations = Field()
    is_sephora_exclusive = Field()
    is_new = Field()
    is_out_of_stock = Field()
    list_price = Field()
    value_price = Field()
    image_urls = Field()
    reviews = Field()
    reviews_count = Field()
    rating = Field()
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
    image_urls = Field()
    is_sephora_exclusive = Field()
    is_new = Field()
    is_out_of_stock = Field()
    url = Field()

# -----------------------------------------------------------------------------

class ReviewItem(BaseItem):
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

class ReviewerItem(BaseItem):
    """Reviewer item"""
    id = Field()
    username = Field()
    location = Field()
    properties = Field()

# END =========================================================================
