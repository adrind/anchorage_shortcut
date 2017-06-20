# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from modelcluster.fields import ParentalKey

from django.db import models
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render
from django.http.response import Http404

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.wagtailforms.models import AbstractForm, AbstractFormField
from wagtail.wagtailcore.url_routing import RouteResult

class TaskChoicesBlock(blocks.StructBlock):
    question = blocks.CharBlock()
    choices = blocks.ListBlock(blocks.StructBlock([
        ('name', blocks.CharBlock(required=True)),
        ('label', blocks.CharBlock(required=True)),
    ],
    template='roadmap/content_blocks/choice_form.html'))

    class Meta:
        label='Add choices to guide a client to services'
        template='roadmap/content_blocks/task_choice_list.html'

class TaskList(Page):
    walk_through_description = RichTextField(blank=True)
    self_service_description = RichTextField(blank=True)
    mrelief_link = models.URLField('Link to external Mrelief form', blank=True)
    choice_list = StreamField([(
        'choices', TaskChoicesBlock()
    )])

    content_panels = Page.content_panels + [
        FieldPanel('walk_through_description', classname='full'),
        FieldPanel('self_service_description', classname='full'),
        FieldPanel('mrelief_link'),
        StreamFieldPanel('choice_list'),
    ]

    def steps(self):
        # Get list of live event pages that are descendants of this page
        events = StepPage.objects.live().descendant_of(self)
        return events

    def route(self, request, path_components):
        if 'walk-through' in path_components:
            # tell Wagtail to call self.serve() with an additional 'path_components' kwarg
            return RouteResult(self, kwargs={'template': 'roadmap/task_list_walk_through.html'})
        else:
            if self.live:
                # tell Wagtail to call self.serve() with no further args
                return RouteResult(self)
            else:
                raise Http404

    def serve(self, request, template=''):
        if template == '':
            template = self.template
        return render(request, template, {
            'page': self
        })


class StepPage(Page):
    header = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('header', classname='title'),
        FieldPanel('body', classname='full'),
    ]