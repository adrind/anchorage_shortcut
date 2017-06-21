# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from modelcluster.fields import ParentalKey

from django.db import models
from django.shortcuts import render
from django.http.response import Http404

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, FieldRowPanel, StreamFieldPanel, InlinePanel
from wagtail.wagtailforms.models import AbstractForm, AbstractFormField
from wagtail.wagtailcore.url_routing import RouteResult
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

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
            return super(TaskList, self).route(request, path_components)

    def serve(self, request, template=''):
        if template == '':
            template = self.template
        return render(request, template, {
            'page': self
        })

class RelatedLink(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField("External link")
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldRowPanel([
            FieldPanel('title', classname='title'),
            FieldPanel('url'),
        ]),
        ImageChooserPanel('image'),
    ]

    class Meta:
        abstract = True

class StepPageRelatedLinks(Orderable, RelatedLink):
    page = ParentalKey('StepPage', related_name='related_links')

class StepPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full'),
        InlinePanel('related_links', label="Related steps"),
    ]
