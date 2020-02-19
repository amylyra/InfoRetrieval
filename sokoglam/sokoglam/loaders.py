# -*- coding: utf-8 -*-

"""Item loaders."""

# Imports =====================================================================

import re
import dateutil.parser

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Identity
from w3lib.html import remove_tags, replace_entities

# Processors ==================================================================

def clean_text(text):
    """Clean text from tags, replace entities and normalize whitespaces."""
    text = remove_tags(str(text))
    text = replace_entities(text)
    return re.sub(r'(\s)+', '\\1', text).strip()

# -----------------------------------------------------------------------------

def parse_date(text):
    """Parse dates from a string into a datetime object."""
    return dateutil.parser.parse(text)

# -----------------------------------------------------------------------------

def parse_float(text):
    """Parse float numbers."""
    return float(text.replace(',', '') if text else 0)

# -----------------------------------------------------------------------------

def parse_int(text):
    """Parse int numbers."""
    return int(text.replace(',', '') if text else 0)

# -----------------------------------------------------------------------------

def parse_bool(text):
    """Parse booleans."""
    return text.lower() in ['true', 'yes']

# Loaders =====================================================================

class ProductItemLoader(ItemLoader):
    """Product item loader."""

    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(clean_text)

    category_out = Join(' > ')
    images_out = Identity()
    tags_out = Identity()

    price_in = MapCompose(clean_text, parse_float)
    price_min_in = MapCompose(clean_text, parse_float)
    price_max_in = MapCompose(clean_text, parse_float)
    review_count_in = MapCompose(clean_text, parse_int)
    rating_in = MapCompose(clean_text, parse_float)
    inventory_quantity_in = MapCompose(clean_text, parse_int)
    published_at_in = MapCompose(clean_text, parse_date)

# -----------------------------------------------------------------------------

class ReviewItemLoader(ItemLoader):
    """Review item loader."""

    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(clean_text)

    date_published_in = MapCompose(clean_text, parse_date)
    rating_in = MapCompose(clean_text, parse_float)
    upvotes_in = MapCompose(clean_text, parse_int)
    downvotes_in = MapCompose(clean_text, parse_int)

# -----------------------------------------------------------------------------

class ReviewerItemLoader(ItemLoader):
    """Reviewer item loader."""

    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(clean_text)

# END =========================================================================
