from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, RichTextFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

class RoadmapSection(blocks.StructBlock):
    title = blocks.CharBlock()
    pages = blocks.ListBlock(blocks.PageChooserBlock())
    image = ImageChooserBlock(required=False)

class HomePage(Page):
    website_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    footer = RichTextField(blank=True)

    header = models.CharField(max_length=255, blank=True)
    mission_statement = models.CharField(max_length=255, blank=True)
    video = models.URLField(max_length=255, blank=True)

    sections = StreamField([
        ('section', RoadmapSection())
    ], blank=True, default=[])

    content_panels = Page.content_panels + [
        ImageChooserPanel('website_icon'),
        RichTextFieldPanel('footer'),
        FieldPanel('header'),
        FieldPanel('mission_statement', classname='full'),
        FieldPanel('video'),
        StreamFieldPanel('sections'),
    ]

    template = 'roadmap/roadmap/base.html'

    def header_title(self):
        return self.title
