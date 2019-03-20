# -*- coding: utf-8 -*-

"""Item loaders."""

# Imports =====================================================================

import re
import datetime
import dateutil.parser

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags, replace_entities

# Processors ==================================================================

def normalize_whitespace(text):
    """Normalize whitespace in text."""
    return re.sub(r'(\s)+', '\\1', text).strip()

# -----------------------------------------------------------------------------

def clean_text(text):
    """Clean text from tags, replace entities and normalize whitespaces."""
    text = remove_tags(str(text))
    text = replace_entities(text)
    return normalize_whitespace(text)

# -----------------------------------------------------------------------------

def parse_date(text):
    """Parse dates from a string into a datetime object."""
    try:
        return dateutil.parser.parse(text)
    except ValueError:
        return datetime.datetime.now()

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

    price_in = MapCompose(clean_text, parse_float)
    category_out = Join(' > ')

# -----------------------------------------------------------------------------

class ReviewItemLoader(ItemLoader):
    """Review item loader."""

    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(clean_text)

# -----------------------------------------------------------------------------

class ReviewerItemLoader(ItemLoader):
    """Reviewer item loader."""

    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(clean_text)

# END =========================================================================
