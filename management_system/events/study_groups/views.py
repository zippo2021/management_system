# -*- coding: utf-8 -*-

from django.shortcuts import render
from events.study_groups.models import StudyGroup
from django.db.models import Q
from events.events_admin.models import Event
from events.events_manage.models import Request
from dashboard.teacher.models import Teacher
from dashboard.regular.models import RegularUser
import json
from django.http import HttpResponse, HttpResponseNotFound
import traceback
from django.core.exceptions import ObjectDoesNotExist


#############
##  VIEWS  ##
#############

def index(request, event_id):
    if request.method == "GET":
        try:
            groups = StudyGroup.objects.filter(event__id=event_id)
            pupils = RegularUser.objects.filter(Request__event__id=event_id, Request__status="Accepted").distinct()
            return render(request, 'study_groups/study_groups_index.html', {'groups': groups, 'event_id': event_id})
        except ObjectDoesNotExist as e:
            return HttpResponseNotFound(request)
        except Exception as e:
            print(traceback.format_exc())
            print(str(e))
            return HttpResponseNotFound(request)

    else:
        return HttpResponseNotFound(request)

###########
##  API  ##
###########


def delete_group(request, event_id):
    if request.method == "POST" and request.is_ajax:
        answer = dict()
        try:
            data = json.loads(request.body.decode('utf-8'))
            StudyGroup.objects.filter(event__id=event_id, id=data).delete()
        except Exception as e:
            print(str(e))
            answer["error"] = "Error: " + str(e)
        return HttpResponse(json.dumps(answer), content_type="application/json")
    else:
        return HttpResponseNotFound(request)


def add_group(request, event_id):
    if request.method == "POST" and request.is_ajax:
        answer = dict()
        try:
            data = json.loads(request.body.decode('utf-8'))
            if data == '':
                raise Exception('Field should be not NULL')
            groups = StudyGroup.objects.filter(event__id=event_id, label=data)
            if len(groups) == 0:
                group = StudyGroup(label=data, event_id=event_id)
                group.save()
                answer["data"] = dict()
                answer["data"]["id"] = group.id
                answer["data"]["name"] = group.label
            else:
                answer["error"] = "Group already exists"
        except Exception as e:
            print(str(e))
            answer["error"] = "Error: " + str(e)
        return HttpResponse(json.dumps(answer), content_type="application/json")
    else:
        return HttpResponseNotFound(request)


def get_group_info(request, event_id):
    if request.method == "POST" and request.is_ajax:
        answer = dict()
        try:
            data = json.loads(request.body.decode('utf-8'))
            pupils_in_group = RegularUser.objects.filter(StudyGroup__id=data, Request__event__id=event_id)\
                .distinct()
            pupils_not_in_group = RegularUser.objects.filter(~Q(StudyGroup__id=data), Request__event__id=event_id)\
                .distinct()
            answer["data"] = dict()
            answer["data"]["in"] = list()
            answer["data"]["out"] = list()
            for pupil in pupils_in_group:
                answer["data"]["in"].append(dict())
                answer["data"]["in"][-1]["id"] = pupil.id
                answer["data"]["in"][-1]["name"] = str(pupil.data)
            for pupil in pupils_not_in_group:
                answer["data"]["out"].append(dict())
                answer["data"]["out"][-1]["id"] = pupil.id
                answer["data"]["out"][-1]["name"] = str(pupil.data)
        except Exception as e:
            print(str(e))
            answer["error"] = "Error: " + str(e)
        return HttpResponse(json.dumps(answer), content_type="application/json")
    else:
        return HttpResponseNotFound(request)


def save_group_members(request, event_id):
    if request.method == "POST" and request.is_ajax:
        answer = dict()
        try:
            data = json.loads(request.body.decode('utf-8'))
            group = StudyGroup.objects.get(id=data["study_group"], event__id=event_id)
            group.users.remove(*RegularUser.objects.filter(id__in=data["pupils"]["remove_from_group"]))
            group.users.add(*RegularUser.objects.filter(id__in=data["pupils"]["add_to_group"]))
            group.save()
        except Exception as e:
            print(traceback.format_exc())
            print(str(e))
            answer["error"] = "Error: " + str(e)
        return HttpResponse(json.dumps(answer), content_type="application/json")
    else:
        return HttpResponseNotFound(request)
