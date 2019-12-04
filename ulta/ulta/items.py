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
    name = Field()
    brand = Field()
    brand_page = Field()
    category = Field()
    short_description = Field()
    long_description = Field()
    price = Field()
    priceCurrency = Field()
    offer_message = Field()
    image = Field()
    bestUses = Field()
    ingredients = Field()
    how_to_use = Field()
    url = Field()
    reviews = Field()
    review_count = Field()
    rating = Field()
    rating_histogram = Field()
    recommended_ratio = Field()
    faceoff_positive = Field()
    faceoff_negative = Field()
    properties = Field()

# -----------------------------------------------------------------------------

class ReviewItem(BaseItem):
    """Review item."""

    id = Field()
    title = Field()
    body = Field()
    rating = Field()
    bottom_line = Field()
    pros = Field()
    cons = Field()
    best_uses = Field()
    reviewer = Field()
    created_at = Field()
    updated_at = Field()
    helpful_votes = Field()
    not_helpful_votes = Field()
    helpful_score = Field()

# -----------------------------------------------------------------------------

class ReviewerItem(BaseItem):
    """Reviewer item."""

    nickname = Field()
    location = Field()
    age = Field()
    badges = Field()
    properties = Field()

# END =========================================================================
