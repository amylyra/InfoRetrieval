# -*- coding: utf-8 -*-

"""Pipelines."""

# Pipelines ===================================================================

class StarReviewsCounterPipeline:
    """Star reviews counter pipeline."""

    # -------------------------------------------------------------------------

    def process_item(self, item, spider):
        """Count star reviews."""
        if not item.get('reviews'):
            return item

        counts = {stars: 0 for stars in [0, 1, 2, 3, 4, 5]}
        for review in item['reviews']:
            counts[review['rating']] = counts.get(review['rating'], 0) + 1
        item['star_reviews_counts'] = counts

        if not item.get('review_count'):
            item['review_count'] = len(item['reviews'])

        if not item.get('rating') and item['review_count'] > 0:
            total = sum([nstar * count for nstar, count in counts.items()])
            item['rating'] = float(total) / item['review_count']

        return item

# END =========================================================================
