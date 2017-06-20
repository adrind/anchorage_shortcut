# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from modelcluster.fields import ParentalKey

from django.db import models
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.wagtailforms.models import AbstractForm, AbstractFormField

class FormField(AbstractFormField):
    page = ParentalKey('TaskList', related_name='form_fields')

class AbstractAdminForm(AbstractForm):
    rules = StreamField([
        ('rules', blocks.StructBlock([
            ('options', blocks.CharBlock()),
            ('page', blocks.PageChooserBlock())])),
    ], blank=True)

    def save(self, *args, **kwargs):
        setattr(self, 'options', self.get_form_fields()[0].choices)
        return super(AbstractAdminForm, self).save(*args, **kwargs)

    def serve(self, request, *args, **kwargs):
        if request.method == 'POST':
            #Hijack the request and redirect according to logic outlined in Wagtail
            options = ','.join(map(lambda x: x.split('=')[1].replace('+', ' '), request.POST.urlencode().split('&')[1:]))
            page = '/'
            for rule in self.rules:
                if rule.value['options'] == options:
                    page = rule.value['page'].url
            return HttpResponsePermanentRedirect(page)

        else:
            form = self.get_form(page=self, user=request.user)
            context = self.get_context(request)
            context['form'] = form
            return render(
                request,
                self.get_template(request),
                context
            )

    class Meta:
        abstract = True


class TaskList(AbstractAdminForm):
    header = models.CharField(max_length=250)
    walk_through_description = RichTextField(blank=True)
    self_service_description = RichTextField(blank=True)

    content_panels = AbstractForm.content_panels + [
        FieldPanel('header', classname="title"),
        FieldPanel('self_service_description', classname="full"),
        FieldPanel('walk_through_description', classname="full"),
        InlinePanel('form_fields', label="Options for this Task"),
        StreamFieldPanel('rules'),
    ]

    def steps(self):
        # Get list of live event pages that are descendants of this page
        events = StepPage.objects.live().descendant_of(self)
        return events

class StepPage(Page):
    header = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('header', classname='title'),
        FieldPanel('body', classname='full'),
    ]