# -*- coding: utf-8 -*-

"""Pipelines"""

# Pipelines ===================================================================

class StarReviewsCounterPipeline(object):
    """Star reviews counter pipeline"""

    # -------------------------------------------------------------------------

    def process_item(self, item, spider):
        """Count star reviews"""
        counts = dict([(stars, 0) for stars in xrange(1, 6)])
        for review in item['reviews']:
            counts[review['rating']] = counts.get(review['rating'], 0) + 1
        item['starReviewsCounts'] = counts

        return item

# END =========================================================================
