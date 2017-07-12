from algoliasearch_django import AlgoliaIndex

class StepIndex(AlgoliaIndex):
    fields = ('short_description', 'title', 'url', 'roadmap')
    settings = {'searchableAttributes': ['short_description', 'body', 'title'], 'attributesForFaceting': ['filterOnly(roadmap)']}
    index_name = 'step_index'

class FaqIndex(AlgoliaIndex):
    fields = ('question', 'answer', 'page_url', 'roadmap')
    settings = {'searchableAttributes': ['question', 'answer'], 'attributesForFaceting': ['filterOnly(roadmap)']}

class StepFaqIndex(FaqIndex):
    index_name = 'step_faq_index'

class TaskListFaqIndex(FaqIndex):
    index_name = 'task_list_faq_index'