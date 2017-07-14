from algoliasearch_django import AlgoliaIndex

class StepIndex(AlgoliaIndex):
    fields = ('short_description', 'title', 'url', 'roadmap', 'live')
    settings = {'searchableAttributes': ['short_description', 'body', 'title'], 'attributesForFaceting': ['filterOnly(roadmap)','filterOnly(live)']}
    index_name = 'step_index'

class FaqIndex(AlgoliaIndex):
    fields = ('question', 'answer', 'url', 'roadmap', 'live')
    settings = {'searchableAttributes': ['question', 'answer'], 'attributesForFaceting': ['filterOnly(roadmap)', 'filterOnly(live)']}

class StepFaqIndex(FaqIndex):
    index_name = 'step_faq_index'

class TaskListFaqIndex(FaqIndex):
    index_name = 'task_list_faq_index'
