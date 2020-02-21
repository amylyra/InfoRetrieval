# -*- coding: utf-8 -*-

"""Items loaders."""

# Imports =====================================================================

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Identity

from realself.utils import clean_text, parse_float, parse_int, parse_date

# Loaders =====================================================================

class TreatmentItemLoader(ItemLoader):
    """Treatment item loader."""

    default_input_processor = MapCompose(clean_text)
    default_output_processor = TakeFirst()

    treated_at_in = MapCompose(clean_text, parse_date)
    reported_cost_in = MapCompose(clean_text, parse_float)

# -----------------------------------------------------------------------------

class ReviewItemLoader(ItemLoader):
    """Review item loader."""

    default_input_processor = MapCompose(clean_text)
    default_output_processor = TakeFirst()

    helpful_count_in = MapCompose(clean_text, parse_int)

    entries_out = Identity()

# -----------------------------------------------------------------------------

class ReviewEntryItemLoader(ItemLoader):
    """Review item loader."""

    default_input_processor = MapCompose(clean_text)
    default_output_processor = TakeFirst()

    published_at_in = MapCompose(clean_text, parse_date)
    helpful_count_in = MapCompose(clean_text, parse_int)

    tags_out = Identity()
    image_urls_out = Identity()

# -----------------------------------------------------------------------------

class ReviewerItemLoader(ItemLoader):
    """Reviewer item loader."""

    default_input_processor = MapCompose(clean_text)
    default_output_processor = TakeFirst()

# -----------------------------------------------------------------------------

class DoctorReviewItemLoader(ItemLoader):
    """Doctor review item loader."""

    default_input_processor = MapCompose(clean_text)
    default_output_processor = TakeFirst()

    rating_in = MapCompose(clean_text, parse_float)

# END =========================================================================
