# -*- coding: utf-8 -*-

"""Pipelines"""

# Pipelines ===================================================================

class StarReviewsCounterPipeline(object):
    """Star reviews counter pipeline"""

    # -------------------------------------------------------------------------

    def process_item(self, item, spider):
        """Count star reviews"""
        counts = {stars: 0 for stars in [1, 2, 3, 4, 5]}
        for review in item['reviews']:
            counts[review['rating']] = counts.get(review['rating'], 0) + 1
        item['starReviewsCounts'] = counts
        return item

# END =========================================================================
