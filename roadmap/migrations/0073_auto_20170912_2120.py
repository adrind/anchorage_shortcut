# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-12 21:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roadmap', '0072_steppage_checklist_instructions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roadmapfrequentlyaskedquestions',
            name='page',
        ),
        migrations.RemoveField(
            model_name='roadmaprelatedresources',
            name='page',
        ),
        migrations.RemoveField(
            model_name='steppagefrequentlyaskedquestions',
            name='page',
        ),
        migrations.RemoveField(
            model_name='steppagerelatedresources',
            name='page',
        ),
        migrations.RemoveField(
            model_name='tasklistfrequentlyaskedquestions',
            name='page',
        ),
        migrations.RemoveField(
            model_name='tasklistrelatedresources',
            name='page',
        ),
        migrations.RemoveField(
            model_name='steppage',
            name='next_step',
        ),
        migrations.RemoveField(
            model_name='tasklist',
            name='header',
        ),
        migrations.DeleteModel(
            name='RoadmapFrequentlyAskedQuestions',
        ),
        migrations.DeleteModel(
            name='RoadmapRelatedResources',
        ),
        migrations.DeleteModel(
            name='StepPageFrequentlyAskedQuestions',
        ),
        migrations.DeleteModel(
            name='StepPageRelatedResources',
        ),
        migrations.DeleteModel(
            name='TaskListFrequentlyAskedQuestions',
        ),
        migrations.DeleteModel(
            name='TaskListRelatedResources',
        ),
    ]
