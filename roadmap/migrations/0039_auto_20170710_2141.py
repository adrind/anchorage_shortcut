# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-10 21:41
from __future__ import unicode_literals

from django.db import migrations
import roadmap.models
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('roadmap', '0038_remove_tasklist_mrelief_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasklist',
            name='choice_list',
        ),
        migrations.RemoveField(
            model_name='tasklist',
            name='choice_rules',
        ),
        migrations.AddField(
            model_name='tasklist',
            name='views',
            field=wagtail.wagtailcore.fields.StreamField((('walk_through_description', wagtail.wagtailcore.blocks.RichTextBlock(default='')), ('self_service_description', wagtail.wagtailcore.blocks.RichTextBlock(default='')), ('choice_list', wagtail.wagtailcore.blocks.StructBlock((('question', wagtail.wagtailcore.blocks.CharBlock()), ('choices', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('label', wagtail.wagtailcore.blocks.CharBlock(required=True)),), template='roadmap/content_blocks/_choice_checkbox.html')))), default=None, label='The options a user can select to discover what steps they should take')), ('rules', wagtail.wagtailcore.blocks.StructBlock((('name', roadmap.models.ChoiceRulesBlock()), ('pages', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.PageChooserBlock()))), label='Rules to define the logic that guides a user to the right Step page'))), null=True),
        ),
    ]
