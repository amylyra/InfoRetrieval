# -*- coding: utf-8 -*-

"""Item loaders."""

# Imports =====================================================================

import re

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

# Loaders =====================================================================

class BaseItemLoader(ItemLoader):
    """Base item loader."""

    default_input_processor = MapCompose(clean_text)
    default_output_processor = TakeFirst()

# -----------------------------------------------------------------------------

class ProductItemLoader(BaseItemLoader):
    """Product item loader."""

    price_in = MapCompose(clean_text, float)
    category_out = Join(' > ')

# -----------------------------------------------------------------------------

class ReviewItemLoader(BaseItemLoader):
    """Review item loader."""

# -----------------------------------------------------------------------------

class ReviewerItemLoader(BaseItemLoader):
    """Reviewer item loader."""

# END =========================================================================
