# -*- coding: utf-8 -*-

"""Item Loaders"""

# Imports =====================================================================

import re
import datetime
import dateutil.parser

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Identity
from w3lib.html import remove_tags, replace_entities

# Processors ==================================================================

def clean_text(text):
    """Clean text from tags, replace entities and normalize whitespaces"""
    text = remove_tags(unicode(text))
    text = replace_entities(text)
    return re.sub(r'(\s)+', '\\1', text).strip()

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

    loves_count_in = MapCompose(clean_text, parse_int)
    reviews_count_in = MapCompose(clean_text, parse_int)
    rating_in = MapCompose(clean_text, parse_float)
    variations_in = Identity()
    variations_out = Identity()

# -----------------------------------------------------------------------------

class ProductVariationItemLoader(ItemLoader):
    """Product variation item loader"""
    default_input_processor = MapCompose(clean_text)
    default_output_processor = TakeFirst()

# -----------------------------------------------------------------------------

class ReviewItemLoader(ItemLoader):
    """Review item loader"""
    default_input_processor = MapCompose(clean_text)
    default_output_processor = TakeFirst()

# -----------------------------------------------------------------------------

class ReviewerItemLoader(ItemLoader):
    """Reviewer item loader"""
    default_input_processor = MapCompose(clean_text)
    default_output_processor = TakeFirst()

# END =========================================================================
