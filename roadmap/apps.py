# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
import algoliasearch_django as algoliasearch
from .index import StepIndex

class RoadmapConfig(AppConfig):
    name = 'roadmap'

    def ready(self):
        StepModel = self.get_model('StepPage')
        algoliasearch.register(StepModel, StepIndex)
