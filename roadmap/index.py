from algoliasearch_django import AlgoliaIndex

class StepIndex(AlgoliaIndex):
    fields = ('short_description', 'title', 'url')
    settings = {'searchableAttributes': ['short_description', 'body', 'title']}
    index_name = 'step_index'

class FaqIndex(AlgoliaIndex):
    fields = ('question', 'answer', 'page_url')
    settings = {'searchableAttributes': ['question', 'answer']}

class StepFaqIndex(FaqIndex):
    index_name = 'step_faq_index'

class TaskListFaqIndex(FaqIndex):
    index_name = 'task_list_faq_index'