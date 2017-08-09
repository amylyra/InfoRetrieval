# -*- coding: utf-8 -*-

"""Item Loaders"""

# Imports =====================================================================

import re
import datetime
import dateutil.parser

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags, replace_entities

# Processors ==================================================================

def clean_text(text):
    """Clean text from tags, replace entities and normalize whitespaces"""
    text = remove_tags(unicode(text))
    text = replace_entities(text)
    # Normalize whitespace
    text = re.sub(r'(\s)+', '\\1', text)
    # Strip whitespace
    return text.strip()

# -----------------------------------------------------------------------------

def parse_date(text):
    """Parse dates from a string into a datetime object"""
    try:
        return dateutil.parser.parse(text)
    except ValueError:
        return datetime.datetime.now()

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
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(clean_text)

    category_out = Join(' > ')
    shipping_out = Join('\n')
    sephoraExclusive_in = MapCompose(clean_text, parse_bool)
    listPrice_in = MapCompose(clean_text, parse_float)
    valuePrice_in = MapCompose(clean_text, parse_float)
    loveCount_in = MapCompose(clean_text, parse_int)
    reviewCount_in = MapCompose(clean_text, parse_int)
    rating_in = MapCompose(clean_text, parse_float)

# -----------------------------------------------------------------------------

class ReviewItemLoader(ItemLoader):
    """Review item loader"""
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(clean_text)

    publishedAt_in = MapCompose(clean_text, parse_date)
    rating_in = MapCompose(clean_text, parse_float)

# -----------------------------------------------------------------------------

class ReviewerItemLoader(ItemLoader):
    """Reviewer item loader"""
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(clean_text)

    reviewDate_in = MapCompose(clean_text, parse_date)

# END =========================================================================
