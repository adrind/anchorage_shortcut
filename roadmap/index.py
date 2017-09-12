from algoliasearch_django import AlgoliaIndex

class StepIndex(AlgoliaIndex):
    fields = ('short_description', 'title', 'url', 'roadmap', 'live')
    settings = {'searchableAttributes': ['short_description', 'body', 'title'], 'attributesForFaceting': ['filterOnly(roadmap)','filterOnly(live)']}
    index_name = 'step_index'