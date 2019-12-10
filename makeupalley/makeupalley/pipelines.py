# -*- coding: utf-8 -*-

"""Item pipelines."""

# Imports =====================================================================

import json

from scrapy.http import Request
from twisted.internet import defer

# Pipelines ===================================================================

class ReviewerLocationExtractorPipeline:
    """Extract reviewer location from profile page."""

    PROFILE_PAGE = 'https://api.makeupalley.com/api/v1/users/%(username)s?scope=full'

    # -------------------------------------------------------------------------

    def __init__(self):
        """Initialize pipeline."""
        self.locations = {}

    # -------------------------------------------------------------------------

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        """Extract reviewer location."""
        for review_index, review in enumerate(item.get('reviews', [])):
            reviewer_username = review['reviewer']['username']

            if self.locations.get(reviewer_username):
                location = self.locations[reviewer_username]
            else:
                response = yield spider.crawler.engine.download(
                    Request(url=self.PROFILE_PAGE % {'username': reviewer_username}),
                    spider
                )

                data = yield json.loads(response.text)

                if response.status == 200:
                    location = {
                        'state': data[0].get('state'),
                        'country': data[0].get('country')
                    }
                    self.locations[reviewer_username] = location
                else:
                    spider.logger.warning(
                        'Item(%s): %s', item['id'], data['message']
                    )
                    location = {}

            item['reviews'][review_index]['reviewer']['state'] = location.get('state')
            item['reviews'][review_index]['reviewer']['country'] = location.get('country')

        defer.returnValue(item)

# =============================================================================

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
