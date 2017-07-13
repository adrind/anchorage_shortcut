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
from wagtail.wagtailcore import hooks

from wagtailgeowidget.edit_handlers import GeoPanel
from django.utils.functional import cached_property
from wagtailgeowidget.helpers import geosgeometry_str_to_struct

from django.utils.html import format_html, format_html_join
from django.conf import settings


#A related website that provides additional assistance
# Used in the roadmap, track, and step templates
class RelatedResource(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField("External link")
    short_description = RichTextField(blank=True)

    panels = [
        FieldRowPanel([
            FieldPanel('title'),
            FieldPanel('url'),
        ]),
        FieldPanel('short_description'),
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

    def url(self):
        return self.page.url

    def roadmap(self):
        return self.page.roadmap()

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
                choicesHtml = choicesHtml + '<button class="selected-choice button bicolor icon icon-cross" data-id="'+choice+'" style="margin:0;margin-right:.5rem;margin-top:.5rem;">One choice</button>'
            out = """<div class="new-choice-button-group"></div><h4><strong>When someone selects:</strong></h4> <div class="selected-choice-container">{}</div><h4><strong>Direct them to these pages:</strong></h4>""".format(choicesHtml)
        else:
            value = 'NEW'
            out = """<div class="new-choice-button-group"></div><h4><strong>When someone selects:</strong></h4> <div class="selected-choice-container">{}</div><h4><strong>Direct them to these pages:</strong></h4>""".format('')

        out = '<div class="sequence-container sequence-type-list choice-list-container" id="'+ prefix +'-container"> <div class="field-content"><input type="hidden" class="selected-choice-input" name="rules-NUM-value-name" value="'+value +'" placeholder="Name" id="rules-NUM-value-name">' + out + '</div></div>'

        return mark_safe(out + '<script>(function(){if (document.readyState === "complete") {return initializeChoices("'+prefix+'");}$(window).load(function() {initializeChoices("'+prefix+'");});})();</script>')

    def value_from_form(self, value):
        arr = value.split(',')
        arr.sort()
        val = ','.join(arr)
        return super(ChoiceRulesBlock, self).value_from_form(val)

class TaskChoicesBlock(blocks.StreamBlock):
    question = blocks.CharBlock()
    choices = blocks.ListBlock(blocks.StructBlock([
        ('label', blocks.CharBlock(required=True)),
    ],
    template='roadmap/task_list/partials/_choice_checkbox.html'))

    class Meta:
        label='Add choices to guide a client to services'
        template='roadmap/task_list/partials/_choice_form.html'

class GuidedSectionBlock(blocks.StreamBlock):
    walk_through_description = blocks.RichTextBlock(default='')
    self_service_description = blocks.RichTextBlock(default='')
    choice_list = TaskChoicesBlock(label='The options a user can select to discover what steps they should take')
    rules = blocks.StructBlock([
        ('name', ChoiceRulesBlock()),
        ('pages', blocks.ListBlock(blocks.PageChooserBlock()))
    ], label='Rules to define the logic that guides a user to the right Step page')

    class Meta:
        label='Add a section to guide users'

class TaskListFrequentlyAskedQuestions(Orderable, FrequentlyAskedQuestion):
    page = ParentalKey('TaskList', related_name='faqs')

class TaskListRelatedResources(Orderable, RelatedResource):
    page = ParentalKey('TaskList', related_name='related_resources')

# A Task List -- contains a series of steps that a user can do to accomplish a specific goal
class TaskList(Page):
    header = models.CharField(max_length=255)
    self_service_oriented_layout = models.BooleanField(default=True)
    short_description = models.CharField(max_length=255, blank=True)
    body = RichTextField(blank=True)

    walk_through_description = RichTextField(blank=True)
    self_service_description = RichTextField(blank=True)

    question = models.CharField(max_length=255, blank=True)
    choices = StreamField([
        ('label', blocks.CharBlock(required=True)),
    ], null=True)

    rules = StreamField([
        ('rule', blocks.StructBlock([
            ('name', ChoiceRulesBlock()),
            ('pages', blocks.ListBlock(blocks.PageChooserBlock()))
        ]))], default=[])

    content_panels = Page.content_panels + [
        FieldPanel('header'),
        FieldPanel('self_service_oriented_layout'),
        FieldPanel('short_description'),
        FieldPanel('body', classname='full'),
        InlinePanel('related_resources', label="Extra resources"),
        InlinePanel('faqs', label="Frequently Asked Questions"),
        MultiFieldPanel([
            FieldPanel('walk_through_description', classname='full'),
            FieldPanel('self_service_description', classname='full'),
            MultiFieldPanel([
                FieldPanel('question'),
                StreamFieldPanel('choices')
            ]),
            StreamFieldPanel('rules')
        ], heading="Guided path for this task", classname="collapsible")
    ]

    template = 'roadmap/task_list/base.html'

    def roadmap(self):
        return self.get_parent().slug

    def steps(self):
        # Get list of all step pages that are descendants of this page
        events = StepPage.objects.live().descendant_of(self)
        return events

    # Directs people to the walk through or self service routes
    # Walk through path uses the choices model to filter steps to take
    def route(self, request, path_components):
        if 'walk-through' in path_components:
            # tell Wagtail to call self.serve() with appropriate template
            return RouteResult(self, kwargs={'template': 'roadmap/task_list/walk_through_page.html'})
        if 'self-service' in path_components:
            return RouteResult(self, kwargs={'template': 'roadmap/task_list/self_service_page.html'})
        else:
            return super(TaskList, self).route(request, path_components)

    def serve(self, request, template=''):
        if template == '':
            template = self.template
        if request.method == 'POST':
            #Get selected checkbox values from form in request - need to strip out csrf token
            selected_choices = list(filter(None, (map(lambda x: x.split('=')[1].replace('+', ' ') if x.split('=')[0] != 'csrfmiddlewaretoken' else '', request.POST.urlencode().split('&')))))

            #Sort the choices so we have them in the same order as the admin defined rules
            selected_choices.sort()
            selected_choices = ','.join(selected_choices)

            #default behavoir is to show all the step pages TODO - allow user to define default in admin
            pages = []
            ids = []

            #loop through each admin defined rule to see if we have a defined rule for the selected choices
            for rule in self.rules:
                if rule.value['name'] == selected_choices:
                    for i, page in enumerate(rule.value['pages']):
                        ids.append(str(page.id))
                        if i+1 < len(rule.value['pages']):
                            #dyanmically set the next step URL for each step page
                            rule.value['pages'][i].next_step = rule.value['pages'][i+1].url
                    pages = rule.value['pages']

            if not ids:
                ids = list(map(str, self.steps().values_list('id', flat=True)))
            return render(request, 'roadmap/task_list/choices_form_result_page.html', {
                'steps': pages,
                'page': self,
                'stepIds' : ','.join(ids)
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

    template = 'roadmap/step/base.html'

    #used to index for search
    def roadmap(self):
        return self.get_parent().get_parent().slug

    @cached_property
    def point(self):
        return geosgeometry_str_to_struct(self.location)

    @property
    def lat(self):
        return self.point['y']

    @property
    def lng(self):
        return self.point['x']

    def serve(self, request):

        ids = request.GET.get('ids')

        if ids:
            ids = ids.split(',')
            steps = []
            index = 0

            for i, id in enumerate(ids):
                steps.append(StepPage.objects.get(id=id))
                if self.id == int(id):
                    index = i + 1

            start = int(len(steps)/2) + 1
            return render(request, self.template, {
                'page': self,
                'stepIds': ','.join(ids),
                'first_half_steps': steps[:start],
                'second_half_steps': steps[start:],
                'step_number': index,
                'start': start
            })

        return render(request, self.template, {
            'page': self
        })


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

    template = 'roadmap/roadmap/base.html'

    def roadmap(self):
        return self.slug

@hooks.register('insert_editor_js')
def editor_js():
    js_files = [
        'js/choices_panel.js',
    ]
    js_includes = format_html_join('\n', '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files)
    )
    return js_includes

