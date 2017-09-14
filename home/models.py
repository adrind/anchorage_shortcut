from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel

class RoadmapSection(blocks.StructBlock):
    title = blocks.CharBlock()
    pages = blocks.ListBlock(blocks.PageChooserBlock())
    image = ImageChooserBlock(required=False)

class HomePage(Page):
    header = models.CharField(max_length=255, blank=True)
    mission_statement = models.CharField(max_length=255, blank=True)
    video = models.URLField(max_length=255, blank=True)

    sections = StreamField([
        ('section', RoadmapSection())
    ], blank=True, default=[])

    testimonials = StreamField([
        ('testimonial', blocks.StructBlock([
            ('quote', blocks.CharBlock()),
            ('name', blocks.CharBlock())
        ]))
    ], blank=True, default=[])

    content_panels = Page.content_panels + [
        FieldPanel('header'),
        FieldPanel('mission_statement', classname='full'),
        FieldPanel('video'),
        StreamFieldPanel('sections'),
        StreamFieldPanel('testimonials'),
    ]

    template = 'roadmap/roadmap/base.html'

    # Used to index
    def roadmap(self):
        return self.slug

