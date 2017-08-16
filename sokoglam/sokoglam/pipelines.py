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
        
        if not item['reviewCount']:
            item['reviewCount'] = len(item['reviews'])
        
        if not item['rating'] and item['reviewCount'] > 0:
            total = sum([nstar * count for nstar, count in counts.items()])
            item['rating'] =  float(total) / item['reviewCount'] 
        
        return item

# END =========================================================================
