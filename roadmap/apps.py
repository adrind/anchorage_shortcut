# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
import algoliasearch_django as algoliasearch
from .index import StepIndex, StepFaqIndex, TaskListFaqIndex

class RoadmapConfig(AppConfig):
    name = 'roadmap'

    def ready(self):
        StepModel = self.get_model('StepPage')
        StepFaqModel = self.get_model('StepPageFrequentlyAskedQuestions')
        TaskListFaqModel = self.get_model('TaskListFrequentlyAskedQuestions')
        algoliasearch.register(StepModel, StepIndex)
        algoliasearch.register(StepFaqModel, StepFaqIndex)
        algoliasearch.register(TaskListFaqModel, TaskListFaqIndex)

