# -*- coding: utf-8 -*-

from base_source_functions import send_templated_email
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from feedback.forms import FeedBackForm
from django.template import Template
from django.template.loader import get_template_from_string
from django.http import HttpResponse

def send(request):
    user = request.user
    if request.method == 'POST':
        form = FeedBackForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            if cleaned_data['problem_type'] == 'T':
                recipients = ['zippo2021@gmail.com']
            else:
                recipients = ['a.s.marchenko@yandex.ru']
            
            text = cleaned_data['text'] + '\n\n\n' + 'From: ' +\
                   user.UserData.__unicode__() + '\n' + 'E-mail: ' +  user.email
            template = get_template_from_string(text)
            send_templated_email(
                subject = cleaned_data['subject'],
                email_context = {},
                recipients = recipients,
                template_file = template,
                fail_silently = False
            )
            status = 'success'
            return HttpResponse(status)

    else:
        form = FeedBackForm()

    return render(request, 'feedback_form.html', {'form': form})
