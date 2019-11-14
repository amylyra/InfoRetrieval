# -*- coding: utf-8 -*-

"""Item Loaders."""

# Imports =====================================================================

import re
import datetime
import dateutil.parser

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
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
    return float(text.replace(',', '') if text else 0.0)

# -----------------------------------------------------------------------------

def parse_int(text):
    """Parse int numbers."""
    return int(text.replace(',', '') if text else 0)

# Loaders =====================================================================

class BaseItemLoader(ItemLoader):
    """Base item loader."""

    default_output_processor = TakeFirst()

# -----------------------------------------------------------------------------

class ProductItemLoader(BaseItemLoader):
    """Product item loader."""

    package_quality_in = MapCompose(parse_float)
    repurchase_percentage_in = MapCompose(parse_int)
    rating_in = MapCompose(parse_float)
    review_count_in = MapCompose(parse_int)

# -----------------------------------------------------------------------------

class ReviewItemLoader(BaseItemLoader):
    """Review item loader."""

    published_at_in = MapCompose(parse_date)
    upvotes_in = MapCompose(parse_int)
    total_votes_in = MapCompose(parse_int)

# -----------------------------------------------------------------------------

class ReviewerItemLoader(BaseItemLoader):
    """Reviewer item loader."""

# END =========================================================================
