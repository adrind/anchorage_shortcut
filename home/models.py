from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from roadmap.models import Roadmap

class HomePage(Page):
    def roadmaps(self):
        # Get list of live event pages that are descendants of this page
        roadmaps = Roadmap.objects.live().descendant_of(self)
        return roadmaps
