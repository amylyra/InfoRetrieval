# -*- coding: utf-8 -*-

"""items loaders."""

# Imports =====================================================================

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Compose

from influenster.utils import clean_text, parse_float, parse_int, parse_date

# Loaders =====================================================================

class ProductItemLoader(ItemLoader):
    """Product item loader."""

    default_input_processor = MapCompose(clean_text)
    default_output_processor = TakeFirst()

    price_in = MapCompose(clean_text, parse_float)
    review_count_in = MapCompose(clean_text, parse_int)
    rating_in = MapCompose(clean_text, parse_float)

    category_out = Join(' > ')
    image_urls_out = Compose(set)

# -----------------------------------------------------------------------------

class ReviewItemLoader(ItemLoader):
    """Review item loader."""

    default_input_processor = MapCompose(clean_text)
    default_output_processor = TakeFirst()

    published_at_in = MapCompose(clean_text, parse_date)
    rating_in = MapCompose(clean_text, parse_float)

# -----------------------------------------------------------------------------

class ReviewerItemLoader(ItemLoader):
    """Reviewer item loader."""

    default_input_processor = MapCompose(clean_text)
    default_output_processor = TakeFirst()

    reviews_count_in = MapCompose(clean_text, parse_int)

    skin_tone_out = Compose(set)
    skin_type_out = Compose(set)
    skin_concerns_out = Compose(set)
    eyes = Compose(set)

# END =========================================================================
