# -*- coding: utf-8 -*-

"""Item pipelines."""

# Pipelines ===================================================================

class StarReviewsCounterPipeline:
    """Star reviews counter pipeline."""

    # -------------------------------------------------------------------------

    def process_item(self, item, spider):
        """Count star reviews."""
        counts = {stars: 0 for stars in [1, 2, 3, 4, 5]}
        for review in item['reviews']:
            if 'rating' not in review:
                continue
            num_stars = int(round(review['rating']))
            counts[review['rating']] = counts.get(num_stars) + 1
        item['starReviewsCounts'] = counts

        if not item['reviewCount']:
            item['reviewCount'] = len(item['reviews'])

        if not item['rating'] and item['reviewCount'] > 0:
            total = sum(nstar * count for nstar, count in counts.items())
            item['rating'] = float(total) / item['reviewCount']

        return item

# END =========================================================================
