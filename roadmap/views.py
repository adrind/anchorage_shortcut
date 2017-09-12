# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import StepPage
# Create your views here.

def print(request):
    pages = request.GET['ids']
    pageIds = pages.split(",")
    steps = []
    for i, id in enumerate(pageIds):
        steps.append(StepPage.objects.get(id=id))

    return render(request, 'roadmap/print.html', {'steps': steps})
