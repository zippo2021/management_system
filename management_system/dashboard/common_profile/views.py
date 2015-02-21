# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dashboard.userdata.models import UserData
from dashboard.common_profile.source_functions import create_info
from dashboard.userdata.documents import docs_to_language
# Create your views here.

@login_required
def view_profile(request,uid):
    restr = True
    if request.user.UserData.id == int(uid):
        user = request.user.UserData
        edit_perm = True
        restr = False
    else:
        user = UserData.objects.get(id = uid)
        edit_perm = False
    base_data = user 
    additional_data = create_info(request.user.UserData, user, restr)
    documents = []
    for each in docs_to_language.keys():
        if hasattr(user, each):
            documents.append(docs_to_language[each])
    if hasattr(user, 'OtherDoc'):
        documents.append(user.OtherDoc.type)
    return render( request, 'common_profile_view_profile.html',
                   {'base_data' : base_data ,
                    'documents' : documents,
                    'additional_data' : additional_data,
                    'edit_perm': edit_perm }
                 )

@login_required
def edit(request,role):
    if role == 'teacher':
        return redirect('teacher_edit')
    elif role == 'regular':
        return redirect('regular_user_wizard')
    else:
        pass
        #FIXME raise exception
