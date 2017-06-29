# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from modelcluster.fields import ParentalKey

from django import forms
from django.db import models
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, FieldRowPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailforms.models import AbstractForm, AbstractFormField
from wagtail.wagtailcore.url_routing import RouteResult
from wagtail.wagtailcore.models import Orderable, Page

from wagtailgeowidget.edit_handlers import GeoPanel
from django.utils.functional import cached_property
from wagtailgeowidget.helpers import geosgeometry_str_to_struct

#A related website that provides additional assistance
# Used in the roadmap, track, and step templates
class RelatedResource(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField("External link")
    description = RichTextField(blank=True)

    panels = [
        FieldRowPanel([
            FieldPanel('title'),
            FieldPanel('url'),
        ]),
        FieldPanel('description'),
    ]

    class Meta:
        abstract = True

# A frequently asked question
# Used in the roadmap, track, and step templates
class FrequentlyAskedQuestion(models.Model):
    question = models.CharField(max_length=255)
    answer = RichTextField()

    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
    ]

    class Meta:
        abstract = True

# Allows admins to create logic that directs users to specific steps
# Used in the track templates
class ChoiceRulesBlock(blocks.CharBlock):
    def __init__(self, required=True, help_text=None, max_length=None, min_length=None,
                 **kwargs):
        super(ChoiceRulesBlock, self).__init__(**kwargs)

    def field(self):
        field_kwargs = {}
        field_kwargs.update(self.field_options)
        return forms.CharField(**field_kwargs)

    def clean(self, value):
        return super(ChoiceRulesBlock, self).clean(value)

    def render_form(self, value, prefix='', errors=None):
        out = ''
        if value:
            choices = value.split(',')
            choicesHtml = ''
            for choice in choices:
                choicesHtml = choicesHtml + '<button class="selected-choice button bicolor icon icon-cross" data-id="'+choice+'">One choice</button>'
            out = """<div class="new-choice-button-group"></div><h4><strong>When someone selects:</strong></h4> <div class="selected-choice-container">{}</div><h4><strong>Direct them to these pages:</strong></h4>""".format(choicesHtml)
        else:
            value = 'NEW'
            out = """<div class="new-choice-button-group"></div><h4><strong>When someone selects:</strong></h4> <div class="selected-choice-container">{}</div><h4><strong>Direct them to these pages:</strong></h4>""".format('')

        out = '<div class="sequence-container sequence-type-list choice-list-container" id="'+ prefix +'-container"> <div class="field-content"><input type="hidden" class="selected-choice-input" name="choice_rules-num-value-name" value="'+value +'" placeholder="Name" id="choice_rules-num-value-name">' + out + '</div></div>'

        return mark_safe(out + '<script src="/static/js/choices_panel.js"></script><script>(function(){if (document.readyState === "complete") {return initializeChoices("'+prefix+'");}$(window).load(function() {initializeChoices("'+prefix+'");});})();</script>')

    def value_from_form(self, value):
        arr = value.split(',')
        arr.sort()
        val = ','.join(arr)
        return super(ChoiceRulesBlock, self).value_from_form(val)

class TaskChoicesBlock(blocks.StructBlock):
    question = blocks.CharBlock()
    choices = blocks.ListBlock(blocks.StructBlock([
        ('label', blocks.CharBlock(required=True)),
    ],
    template='roadmap/content_blocks/_choice_checkbox.html'))

    class Meta:
        label='Add choices to guide a client to services'
        template='roadmap/content_blocks/_choice_form.html'

class TaskListFrequentlyAskedQuestions(Orderable, FrequentlyAskedQuestion):
    page = ParentalKey('TaskList', related_name='faqs')

class TaskListRelatedResources(Orderable, RelatedResource):
    page = ParentalKey('TaskList', related_name='related_resources')

# A Task List -- contains a series of steps that a user can do to accomplish a specific goal
class TaskList(Page):
    header = models.CharField(max_length=255)
    isTemplateA = models.BooleanField(default=True)
    body = RichTextField(blank=True)
    walk_through_description = RichTextField(blank=True)
    self_service_description = RichTextField(blank=True)
    mrelief_link = models.URLField('Link to external Mrelief form', blank=True)
    choice_list = StreamField([(
        'choices', TaskChoicesBlock()
    )])
    choice_rules = StreamField([
        ('rules', blocks.StructBlock([
            ('name', ChoiceRulesBlock()),
            ('pages', blocks.ListBlock(blocks.PageChooserBlock()))
        ])),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('header'),
        FieldPanel('isTemplateA'),
        FieldPanel('body', classname='full'),
        FieldPanel('walk_through_description', classname='full'),
        FieldPanel('self_service_description', classname='full'),
        FieldPanel('mrelief_link'),
        StreamFieldPanel('choice_list'),
        StreamFieldPanel('choice_rules'),
        InlinePanel('related_resources', label="Extra resources"),
        InlinePanel('faqs', label="Frequently Asked Questions"),
    ]

    template = 'roadmap/task_list/base.html'

    def steps(self):
        # Get list of all step pages that are descendants of this page
        events = StepPage.objects.live().descendant_of(self)
        return events

    # Directs people to the walk through or self service routes
    # Walk through path uses the choices model to filter steps to take
    def route(self, request, path_components):
        if 'walk-through' in path_components:
            # tell Wagtail to call self.serve() with appropriate template
            return RouteResult(self, kwargs={'template': 'roadmap/task_list/walk_through.html'})
        if 'self-service' in path_components:
            return RouteResult(self, kwargs={'template': 'roadmap/task_list/self_service.html'})
        else:
            return super(TaskList, self).route(request, path_components)

    def serve(self, request, template=''):
        if template == '':
            template = self.template
        if request.method == 'POST':
            arr = filter(None, (map(lambda x: x.split('=')[1].replace('+', ' ') if x.split('=')[0] != 'csrfmiddlewaretoken' else '', request.POST.urlencode().split('&'))))
            arr.sort()
            options = ','.join(arr)
            pages = []
            for rule in self.choice_rules:
                if rule.value['name'] == options:
                    for i, page in enumerate(rule.value['pages']):
                        if i+1 < len(rule.value['pages']):
                            rule.value['pages'][i].next_step = rule.value['pages'][i+1].url
                    pages = rule.value['pages']

            return render(request, 'roadmap/task_list/choices.html', {
                'steps': pages,
                'page': self
            })

        return render(request, template, {
            'page': self
        })

class StepPageFrequentlyAskedQuestions(Orderable, FrequentlyAskedQuestion):
    page = ParentalKey('StepPage', related_name='faqs')

class StepPageRelatedResources(Orderable, RelatedResource):
    page = ParentalKey('StepPage', related_name='related_resources')

class StepPage(Page):
    short_description = models.CharField(max_length=255)
    body = RichTextField(blank=True)
    next_step = models.URLField(blank=True)

    address = models.CharField(max_length=250, blank=True, null=True)
    location = models.CharField(max_length=250, blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('short_description', classname='full'),
        FieldPanel('body', classname='full'),
        InlinePanel('related_resources', label='Extra resources'),
        InlinePanel('faqs', label='Frequently asked questions'),
        MultiFieldPanel([
            FieldPanel('address'),
            GeoPanel('location', address_field='address'),
        ], _('Geo details')),
    ]

    @cached_property
    def point(self):
        return geosgeometry_str_to_struct(self.location)

    @property
    def lat(self):
        return self.point['y']

    @property
    def lng(self):
        return self.point['x']

class RoadmapFrequentlyAskedQuestions(Orderable, FrequentlyAskedQuestion):
    page = ParentalKey('Roadmap', related_name='faqs')

class RoadmapRelatedResources(Orderable, RelatedResource):
    page = ParentalKey('Roadmap', related_name='related_resources')

class Roadmap(Page):
    header = models.CharField(max_length=255)
    body = RichTextField(blank=True)
    sections = StreamField([
        ('section', blocks.StructBlock([
            ('title', blocks.CharBlock()),
            ('pages', blocks.ListBlock(blocks.PageChooserBlock()))
        ])),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('header'),
        FieldPanel('body', classname='full'),
        StreamFieldPanel('sections'),
        InlinePanel('related_resources', label='Extra resources'),
        InlinePanel('faqs', label='Frequently asked questions'),
    ]
