# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse, Http404
	
from django.contrib import messages

# decorator for built-in auth system
from django.contrib.auth.decorators import login_required

from django.db import transaction

from django.contrib.auth.models import User

from .. forms import *
from .. models import *
import datetime
from django.utils import timezone


def process_button(request, status):
	if request.method == 'POST':
		task_id = request.POST.get('task_id')
		status = request.POST.get('status')

		task_info = get_object_or_404(TaskInfo, pk=task_id)
		if not task_info:
			raise Http404

		if status == 'true':
			task_info.time_spent = (timezone.now() - task_info.continue_time) + task_info.time_spent
			task_info.save()

		if status == 'false':
			task_info.continue_time = timezone.now()
			task_info.save()

def process_stop(request):
	if request.method == 'POST':
		task_id = request.POST.get('task_id')

		task_info = get_object_or_404(TaskInfo, pk = task_id)
		if not task_info:
			raise Http404

		task_info.time_spent = (timezone.now() - task_info.continue_time) + task_info.time_spent
		task_info.stop_time = timezone.now()


