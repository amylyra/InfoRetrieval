# -*- coding: utf-8 -*-

"""Item Loaders"""

# Imports =====================================================================

import re
import dateutil.parser

import html2text
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Identity, Join
from w3lib.html import remove_tags, replace_entities

# Processors ==================================================================

def normalize_whitespace(text):
    """Normalize whitespace"""
    return re.sub(r'(\s)+', '\\1', text, flags=re.UNICODE).strip()

# -----------------------------------------------------------------------------

def clean_text(text):
    """Clean text from tags, replace entities and normalize whitespaces"""
    text = remove_tags(str(text))
    text = replace_entities(text)
    return normalize_whitespace(text)

# -----------------------------------------------------------------------------

def to_markdown(html):
    """Convert HTML to markdown formatted text"""
    parser = html2text.HTML2Text()
    parser.body_width = 0 # no wrapping
    text = parser.handle(html)
    return normalize_whitespace(text)

# -----------------------------------------------------------------------------

def parse_date(text):
    """Parse dates from a string into a datetime object"""
    return dateutil.parser.parse(text)

# -----------------------------------------------------------------------------

def parse_float(text):
    """Parse float numbers"""
    return float(text.replace(',', '') if text else 0)

# -----------------------------------------------------------------------------

def parse_int(text):
    """Parse int numbers"""
    return int(text.replace(',', '') if text else 0)

# -----------------------------------------------------------------------------

def parse_bool(text):
    """Parse booleans"""
    return text.lower() in ['true', 'yes']

# Loaders =====================================================================

class ProductItemLoader(ItemLoader):
    """Product item loader"""
    default_input_processor = MapCompose(clean_text)
    default_output_processor = TakeFirst()

    category_out = Join(' > ')
    description_in = MapCompose(to_markdown)
    warnings_in = MapCompose(to_markdown)
    shipping_in = MapCompose(to_markdown)
    ingredients_in = MapCompose(to_markdown)
    reviews_count_in = MapCompose(clean_text, parse_int)
    rating_in = MapCompose(clean_text, parse_float)

    image_urls_in = Identity()
    image_urls_out = Identity()

# -----------------------------------------------------------------------------

class ReviewItemLoader(ItemLoader):
    """Review item loader"""
    default_input_processor = MapCompose(clean_text)
    default_output_processor = TakeFirst()

    published_at_in = MapCompose(clean_text, parse_date)
    rating_in = MapCompose(clean_text, parse_float)
    is_featured_in = MapCompose(clean_text, parse_bool)
    positive_feedback_count_in = MapCompose(clean_text, parse_int)
    negative_feedback_count_in = MapCompose(clean_text, parse_int)
    reviewer_in = Identity()

# -----------------------------------------------------------------------------

class ReviewerItemLoader(ItemLoader):
    """Reviewer item loader"""
    default_input_processor = MapCompose(clean_text)
    default_output_processor = TakeFirst()

    properties_in = Identity()
    properties_out = Identity()

# END =========================================================================
