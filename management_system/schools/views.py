# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from schools.forms import SchoolForm
from schools.models import School
from django.http import HttpResponse
from decorators import should_be_admin
import json
from schools import school_list
# Create your views here.

def transfer(request):
    for each in school_list.school_choices:
        name = each[0]
        list_ = name.split('г.')
        v_name = list_[0]
        v_name = v_name.strip()
        if len(list_) >1:         
            city = list_[1]
            city = city.strip()
        else:
            city = "Город N"
        country = 'Россия'
        school = School(name=v_name, country=country, city = city)
        school.save()
    return HttpResponse('vasa')

@login_required
@should_be_admin
def add(request):
    if request.method == 'POST':
        form = SchoolForm(request.POST)
        if form.is_valid():
            school = form.save()
            status = "success"
            school_id = school.id
            return HttpResponse(json.dumps({'status':status,'school_id':school_id}))
    else:       
        form = SchoolForm()
    return render(request, 'schools_add_form.html', {'form' : form})
    

@login_required
@should_be_admin
def edit(request, school_id):
    school = School.objects.get(id = school_id)
    if request.method == 'POST':
        form = SchoolForm(request.POST, instance = school)
        if form.is_valid():
            school = form.save(commit=False)
            school.approved = True
            school.save()
            status="success"
            return HttpResponse(status)
    else:       
        form = SchoolForm(instance = school)
    return render(request, 'schools_edit_form.html', {'form' : form})

@login_required
@should_be_admin
def approve(request, school_id):
    school = School.objects.get(id = school_id)
    school.approved = True
    school.save()
    return redirect('schools_show_unproved')

@login_required
@should_be_admin
def show_unproved(request):
    schools = School.objects.filter(approved = False)
    return render(request, 'schools_show_unproved.html', {'schools' : schools})
