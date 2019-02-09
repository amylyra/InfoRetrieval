# -*- coding: utf-8 -*-

"""Pipelines"""

# Pipelines ===================================================================

class StarReviewsCounterPipeline(object):
    """Star reviews counter pipeline"""

    # -------------------------------------------------------------------------

    def process_item(self, item, spider):
        """Count star reviews"""
        counts = {star: 0 for star in [1, 2, 3, 4, 5]}
        if item.get('reviews'):
            for review in item['reviews']:
                counts[review['rating']] += 1
        item['star_reviews_counts'] = counts
        return item

# END =========================================================================
