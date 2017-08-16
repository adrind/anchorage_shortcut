from __future__ import absolute_import, unicode_literals

from django.http import HttpResponseRedirect

from wagtail.wagtailcore.models import Page
from roadmap.models import Roadmap

class HomePage(Page):
    def roadmaps(self):
        # Get list of live event pages that are descendants of this page
        roadmaps = Roadmap.objects.live().descendant_of(self)
        return roadmaps

    #TODO: Remove code after soft launch -- temporary redirect
    def serve(self, request):
        return HttpResponseRedirect("/job-checklist/")

