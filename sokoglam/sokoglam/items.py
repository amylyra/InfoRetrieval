# -*- coding: utf-8 -*-

"""Items."""

# Imports =====================================================================

from scrapy import Item, Field

# Items =======================================================================

class BaseItem(Item):
    """Base item."""

# -----------------------------------------------------------------------------

class ProductItem(BaseItem):
    """Product item."""

    id = Field()
    sku = Field()
    barcode = Field()
    name = Field()
    type = Field()
    brand = Field()
    description = Field()
    tags = Field()
    handle = Field()
    price_currency = Field()
    price = Field()
    price_min = Field()
    price_max = Field()
    featured_image = Field()
    images = Field()
    video = Field()
    how_to = Field()
    staff_review = Field()
    category = Field()
    review_count = Field()
    rating = Field()
    key_ingredients = Field()
    full_ingredients = Field()
    availability = Field()
    inventory_quantity = Field()
    published_at = Field()
    url = Field()
    reviews = Field()
    star_reviews_counts = Field()

# -----------------------------------------------------------------------------

class ReviewItem(BaseItem):
    """Review item."""

    title = Field()
    description = Field()
    rating = Field()
    date_published = Field()
    upvotes = Field()
    downvotes = Field()
    reviewer = Field()

# -----------------------------------------------------------------------------

class ReviewerItem(BaseItem):
    """Reviewer item."""

    name = Field()
    age = Field()
    skin_type = Field()
    verified_buyer = Field()

# END =========================================================================
