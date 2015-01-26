# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dashboard.common_profile.permissions import field_perms
from user_manager.permissions import perms_to_classes
# Create your views here.

def perms_to_list(perms):
    result = []
    for key in perms:
        if perms[key]:
            print perms[key]
            result.append(perms_to_classes[key])
    return result


def create_info(viewer,user,restr):
    result = {"Teacher":{},"RegularUser":{},"Observer":{},"Mentor":{}}
    viewer_perms = perms_to_list(viewer.UserData.get_permissions())
    user_perms = perms_to_list(user.UserData.get_permissions())
    if restr:
        for uperm in user_perms:
            for key in field_perms[uperm]:
                if list(set(field_perms[uperm][key]) & set(viewer_perms)):
                    result[uperm][key] = getattr(getattr(user.UserData,uperm),key)            
    else:
        for uperm in user_perms:
            for key in field_perms[uperm]:
                result[uperm][key] = getattr(getattr(user.UserData,uperm),key)       
    print result
    return result

@login_required
def view_profile(request,uid):
    restr = True
    if request.user.id == int(uid):
        user = request.user
        edit_perm = True
        restr = False
    else:
        user = User.objects.get(id = uid)
        edit_perm = False
    print user.UserData.get_permissions()
    base_data = user.UserData
 
    additional_data = create_info(request.user,user,restr)
    
    print additional_data
    return render( request, 'view_profile.html' , {'base_data' : base_data , 'additional_data' : additional_data, 'edit_perm':edit_perm })
