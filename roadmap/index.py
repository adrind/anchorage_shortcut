from algoliasearch_django import AlgoliaIndex

class StepIndex(AlgoliaIndex):
    fields = ('short_description', 'title', 'url', 'live', 'page_body')
    settings = {'searchableAttributes': ['short_description', 'page_body', 'title'], 'attributesForFaceting': ['filterOnly(live)']}
    index_name = 'step_index'