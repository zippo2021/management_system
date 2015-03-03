# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from search.forms import UserSearchForm
from dashboard.userdata.models import UserData
from django.http import HttpResponse


def user_search(request):
    user = request.user
    if request.method == 'POST':
        form = UserSearchForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            first_name = cleaned_data['first_name'].strip()
            last_name = cleaned_data['last_name'].strip()
            result = dict()
            users = None
            status = "None"
            if last_name == "" and first_name == "":
                print(1)
                pass
            elif last_name == "" and first_name != "":
                print(2)
                users = UserData.objects.filter(first_name=first_name)
                if len(users) > 0:
                    status = "Get"
            elif last_name != "" and first_name == "":
                print(3)
                users = UserData.objects.filter(last_name=last_name)
                if len(users) > 0:
                    status = "Get"
            elif last_name != "" and first_name != "":
                users = UserData.objects.filter(first_name=first_name, last_name=last_name)
                if len(users) > 0:
                    status = "Get"
            return render(request, 'user_search_result.html', {'users': users, 'status': status})
    else:
        form = UserSearchForm()

    return render(request, 'user_search_form.html', {'form': form})
