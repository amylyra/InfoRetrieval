# -*- coding: utf-8 -*-

"""Items."""

# Imports =====================================================================

from scrapy import Item, Field

# Items =======================================================================

class TreatmentItem(Item):
    """Treatment item."""

    id = Field()
    name = Field()
    treated_at = Field()
    reported_cost = Field()
    worth_it = Field()

# -----------------------------------------------------------------------------

class ReviewItem(Item):
    """Review item."""

    id = Field()
    title = Field()
    url = Field()
    tags = Field()
    helpful_count = Field()
    entries = Field()
    treatment = Field()
    reviewer = Field()
    doctor_review = Field()

# -----------------------------------------------------------------------------

class ReviewEntryItem(Item):
    """Review item."""

    id = Field()
    title = Field()
    body = Field()
    published_at = Field()
    tags = Field()
    helpful_count = Field()
    image_urls = Field()

# -----------------------------------------------------------------------------

class ReviewerItem(Item):
    """Reviewer item."""

    id = Field()
    username = Field()
    avatar_url = Field()
    profile_url = Field()

# -----------------------------------------------------------------------------

class DoctorReviewItem(Item):
    """Doctor review item."""

    id = Field()
    name = Field()
    title = Field()
    location = Field()
    avatar_url = Field()
    profile_url = Field()
    review = Field()
    rating = Field()

# END =========================================================================
