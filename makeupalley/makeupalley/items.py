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
    name = Field()
    brand = Field()
    image = Field()
    category = Field()
    package_quality = Field()
    repurchase_percentage = Field()
    review_count = Field()
    rating = Field()
    url = Field()
    reviews = Field()
    star_reviews_counts = Field()

# -----------------------------------------------------------------------------

class ReviewItem(BaseItem):
    """Review item."""

    id = Field()
    content = Field()
    rating = Field()
    published_at = Field()
    upvotes = Field()
    total_votes = Field()
    reviewer = Field()

# -----------------------------------------------------------------------------

class ReviewerItem(BaseItem):
    """Reviewer item."""

    username = Field()
    skin_type = Field()
    skin_tone = Field()
    skin_undertone = Field()
    hair_color = Field()
    hair_type = Field()
    hair_texture = Field()
    eye_color = Field()
    age_range = Field()
    state = Field()
    country = Field()
    reviews_count = Field()

# END =========================================================================
