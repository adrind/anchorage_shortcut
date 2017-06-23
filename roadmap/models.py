# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from modelcluster.fields import ParentalKey

from django import forms
from django.db import models
from django.shortcuts import render
from django.http.response import Http404
from django.forms import HiddenInput
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.functional import cached_property

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, FieldRowPanel, StreamFieldPanel, InlinePanel, BaseFieldPanel
from wagtail.wagtailforms.models import AbstractForm, AbstractFormField
from wagtail.wagtailcore.url_routing import RouteResult
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel


class ChoicesField(HiddenInput):
    def __init__(self, *args, **kwargs):
        super(ChoicesField, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        out = super(ChoicesField, self).render(name, value, attrs)
        return mark_safe('<div id="button-group">Hi</p>' + '''            
             <script>
            (function(){
                if (document.readyState === 'complete') {
                    return initializeChoices();
                }
                $(window).load(function() {
                    initializeChoices();
                });
            })();
            </script>
            ''')

    class Media:
        js = (
            'js/choices_panel.js',
        )

class ChoiceRulesBlock(blocks.CharBlock):
    def __init__(self, required=True, help_text=None, max_length=None, min_length=None,
                 **kwargs):
        self.field_options = {'widget': ChoicesField()}
        super(ChoiceRulesBlock, self).__init__(**kwargs)

    def field(self):
        field_kwargs = {'widget': ChoicesField()}
        field_kwargs.update(self.field_options)
        return forms.CharField(**field_kwargs)

    def clean(self, value):
        return super(ChoiceRulesBlock, self).clean(value)

    def render_form(self, value, prefix='', errors=None):
        out = '<div id="button-group"></div>'
        if value:
            out += '<p>When someone selects:</p> <div class="selected-choice-container">'
            choices = value.split(',')
            for choice in choices:
                out = out + '<button class="selected-choice button bicolor icon icon-cross" data-id="'+choice+'">One choice</button>'
            out += '</div><p>Direct them to these pages:</p>'
        else:
            value = 'NEW'

        out = '<div class="sequence-container sequence-type-list choice-list-container"> <div class="field-content"><input type="hidden" class="selected-choice-input" name="choice_rules-num-value-name" value="'+value +'" placeholder="Name" id="choice_rules-num-value-name">' + out + '</div></div>'

        return mark_safe(out + '''            
             <script>
            (function(){
                if (document.readyState === 'complete') {
                    return initializeChoices();
                }
                $(window).load(function() {
                    initializeChoices();
                });
            })();
            </script>
            <script src="/static/js/choices_panel.js"></script>
            ''')

    def value_from_form(self, value):
        arr = value.split(',')
        arr.sort()
        val = ','.join(arr)
        return super(ChoiceRulesBlock, self).value_from_form(val)

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
    choice_rules = StreamField([
        ('rules', blocks.StructBlock([
            ('name', ChoiceRulesBlock()),
            ('pages', blocks.ListBlock(blocks.PageChooserBlock()))
        ])),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('walk_through_description', classname='full'),
        FieldPanel('self_service_description', classname='full'),
        FieldPanel('mrelief_link'),
        StreamFieldPanel('choice_list'),
        StreamFieldPanel('choice_rules'),
    ]

    def steps(self):
        # Get list of live event pages that are descendants of this page
        events = StepPage.objects.live().descendant_of(self)
        return events

    def route(self, request, path_components):
        if 'walk-through' in path_components:
            # tell Wagtail to call self.serve() with appropriate template
            return RouteResult(self, kwargs={'template': 'roadmap/task_list_walk_through.html'})
        if 'self-service' in path_components:
            return RouteResult(self, kwargs={'template': 'roadmap/task_list_self_service.html'})
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

            return render(request, 'roadmap/choices.html', {
                'pages': pages
            })

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
    next_step = models.URLField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full'),
        InlinePanel('related_links', label="Related steps"),
    ]

class Roadmap(Page):
    body = RichTextField(blank=True)
    sections = StreamField([
        ('section', blocks.StructBlock([
            ('title', blocks.CharBlock()),
            ('pages', blocks.ListBlock(blocks.PageChooserBlock()))
        ])),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full'),
        StreamFieldPanel('sections'),
    ]
