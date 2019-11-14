# -*- coding: utf-8 -*-

"""Item pipelines."""

# Pipelines ===================================================================

class StarReviewsCounterPipeline:
    """Star reviews counter pipeline."""

    # -------------------------------------------------------------------------

    def process_item(self, item, spider):
        """Count star reviews."""
        counts = {stars: 0 for stars in [1, 2, 3, 4, 5]}
        for review in item.get('reviews', []):
            if not review.get('rating'):
                continue
            rounded_stars = int(round(review['rating']))
            counts[review['rating']] = counts.get(rounded_stars) + 1
        item['star_reviews_counts'] = counts
        return item

# END =========================================================================
