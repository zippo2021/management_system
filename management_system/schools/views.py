# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from schools.forms import SchoolForm
from schools.models import School
from django.http import HttpResponse
from decorators import should_be_defined, should_be_regular
# Create your views here.

@login_required
@should_be_defined
def add(request):
    if request.method == 'POST':
        form = SchoolForm(request.POST)
        if form.is_valid():
            school = form.save()
            status = "success"
            return HttpResponse(status)
    else:       
        form = SchoolForm()
    return render(request, 'schools_add_form.html', {'form' : form})
    

@login_required
@staff_member_required
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
@staff_member_required
def approve(request, school_id):
    school = School.objects.get(id = school_id)
    school.approved = True
    school.save()
    return redirect('schools_show_unproved')

@login_required
@staff_member_required
def show_unproved(request):
    schools = School.objects.filter(approved = False)
    return render(request, 'schools_show_unproved.html', {'schools' : schools})
