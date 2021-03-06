# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse, Http404

# decorator for built-in auth system
from django.contrib.auth.decorators import login_required

from django.db import transaction

from .. forms import *
from .. models import *


# Create your views here.
@login_required
def dashboard(request):
    context = {}
    add_course_form = CourseForm()
    course_task_form = CourseTaskForm()
    research_form = ResearchForm()
    routine_form = MiscForm()
    task_info_form = TaskInfoForm()
    context['add_course_form'] = add_course_form
    context['course_task_form'] = course_task_form
    context['research_form'] = research_form
    context['routine_form'] = routine_form
    context['task_info_form'] = task_info_form
    courses = Course.objects.filter(user=request.user)
    context['course_names'] = courses
    context['course_tasks'] = []

    for course in courses:
        tasks = CourseTask.objects.filter(course=course)
        for task in tasks:
            if task.task_info.status != 2:
                context['course_tasks'].append(task)

    context['research_tasks'] = Research.objects.filter(user=request.user).exclude(task_info__status=2)
    context['routine_tasks'] = Misc.objects.filter(user=request.user).exclude(task_info__status=2)
    context['username'] = request.user.username

    return render(request, 'dashboard/current_tasks.html', context)


def edit_course_modal(request, task_id, task_info_id):
    course_task = get_object_or_404(CourseTask, pk=task_id)
    if not course_task:
        raise Http404

    task_info = get_object_or_404(TaskInfo, pk=task_info_id)
    if not task_info:
        raise Http404

    task_info_form = TaskInfoForm(instance=task_info)
    course_task_form = CourseTaskForm(instance=course_task)
    context = dict()
    context['course_task_form'] = course_task_form
    context['task_info_form'] = task_info_form
    context['task_id'] = task_id
    context['task_info_id'] = task_info_id
    response = render_to_string('modals/edit_course_modal.html', context, request=request)
    return HttpResponse(response)


def edit_research_modal(request, task_id, task_info_id):
    research_task = get_object_or_404(Research, pk=task_id)
    if not research_task:
        raise Http404

    task_info = get_object_or_404(TaskInfo, pk=task_info_id)
    if not task_info:
        raise Http404

    task_info_form = TaskInfoForm(instance=task_info)
    research_form = ResearchForm(instance=research_task)
    context = dict()
    context['research_form'] = research_form
    context['task_info_form'] = task_info_form
    context['task_id'] = task_id
    context['task_info_id'] = task_info_id
    response = render_to_string('modals/edit_research_modal.html', context, request=request)
    return HttpResponse(response)


def edit_routine_modal(request, task_id, task_info_id):
    routine_task = get_object_or_404(Misc, pk=task_id)
    if not routine_task:
        raise Http404

    task_info = get_object_or_404(TaskInfo, pk=task_info_id)
    if not task_info:
        raise Http404

    task_info_form = TaskInfoForm(instance=task_info)
    routine_form = MiscForm(instance=routine_task)
    context = dict()
    context['routine_form'] = routine_form
    context['task_info_form'] = task_info_form
    context['task_id'] = task_id
    context['task_info_id'] = task_info_id
    response = render_to_string('modals/edit_routine_modal.html', context, request=request)
    return HttpResponse(response)
