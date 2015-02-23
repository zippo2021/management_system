# -*- coding: utf-8 -*-
from dashboard.teacher.models import Teacher
from events.events_admin.models import Event
from dashboard.regular.models import RegularUser
from events.study_groups.models import StudyGroup
from events.journal.models import Lesson, Subject, Homework, Mark
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
import json
from datetime import datetime, timedelta


def get_date_in_range(start, end, step=1):
    result = list()
    cur = start
    while cur <= end:
        result.append(cur)
        cur += timedelta(days=step)
    return result


def get_date_count(start, count=1, step=1):
    result = list()
    cur = start
    for i in range(0, count):
        result.append(cur)
        cur += timedelta(days=step)
    return result


def get_groups(data):
    answer = list()
    groups = StudyGroup.objects.filter(event__id=data["event_id"],
                                       lesson__teacher__id=int(data["teacher"]),
                                       lesson__subject__id=int(data["subject"])).distinct()
    for group in groups:
        answer.append(dict())
        answer[-1]["id"] = group.id
        answer[-1]["name"] = group.label
    return answer


def get_pupils(data):
    answer = list()
    pupils = RegularUser.objects.filter(StudyGroup__id=data["group"],
                                        Request__event__id=data["event_id"]).order_by("data__last_name")
    for pupil in pupils:
        answer.append(dict())
        answer[-1]["name"] = str(pupil.data)
        answer[-1]["id"] = pupil.id
    return answer


def get_lessons(data):
    print(data)
    dates = get_date_in_range(datetime.strptime(data["start_date"], '%d/%m/%Y').date(),
                              datetime.strptime(data["end_date"], '%d/%m/%Y').date(),
                              1)
    lessons = Lesson.objects.filter(group__id=int(data["group"]),
                                    teacher__id=int(data["teacher"]),
                                    subject__id=int(data['subject']),
                                    date__in=dates,
                                    event__id=int(data["event_id"])).order_by("date", "start_time")
    answer = list()
    for lesson in lessons:
        homeworks = Homework.objects.filter(to_lesson=lesson)
        answer.append(dict())
        answer[-1]["id"] = lesson.id
        answer[-1]["date"] = lesson.date.strftime('%d/%m/%Y')
        answer[-1]["start_time"] = lesson.start_time.strftime('%H:%M')
        answer[-1]["end_time"] = lesson.end_time.strftime('%H:%M')
        answer[-1]["group"] = lesson.group.label
        answer[-1]["title"] = lesson.title
        answer[-1]["comment"] = lesson.comment if lesson.comment is not None else ""
        answer[-1]["subject"] = lesson.subject.name
        answer[-1]["place"] = lesson.place
        answer[-1]["homework"] = ""
        answer[-1]["homework_comment"] = ""
        answer[-1]["homework_id"] = ""
        if len(homeworks) > 0:
            answer[-1]["homework"] = homeworks[0].title
            answer[-1]["homework_comment"] = homeworks[0].comment
            answer[-1]["homework_id"] = homeworks[0].id
    return answer


def get_marks(data):
    answer = dict()
    pupils_ids = list(pupil["id"] for pupil in data["pupils"])
    lessons_ids = list(lesson["id"] for lesson in data["lessons"])
    for pid in pupils_ids:
        answer[pid] = dict()
        for lid in lessons_ids:
            answer[pid][lid] = ""
    marks = Mark.objects.filter(pupil__id__in=pupils_ids, lesson__id__in=lessons_ids).distinct()
    for mark in marks:
        answer[mark.pupil.id][mark.lesson.id] = mark.mark
    return answer


###########
##  API  ##
###########


def set_mark(request, event_id):
    if request.method == "POST" and request.is_ajax:
        answer = dict()
        answer["data"] = list()
        try:
            data = json.loads(request.body.decode('utf-8'))
            try:
                mark = Mark.objects.get(pupil__id=data["pupil"], lesson__id=data["lesson"])
                if data["mark"] == "":
                    mark.delete()
                else:
                    mark.mark = int(data["mark"])
                    mark.save()
            except Mark.DoesNotExist:
                if data["mark"] != "":
                    mark = Mark(mark=int(data["mark"]))
                    mark.lesson = Lesson.objects.get(id=data["lesson"])
                    mark.pupil = RegularUser.objects.get(id=data["pupil"])
                    mark.save()
        except Exception as e:
            print(str(e))
            answer["error"] = "Error: " + str(e)
        return HttpResponse(json.dumps(answer), content_type="application/json")
    else:
        return HttpResponseNotFound(request)


def get_pupils_lessons_marks(request, event_id):
    if request.method == "POST" and request.is_ajax:
        answer = dict()
        answer["data"] = dict()
        try:
            data = json.loads(request.body.decode('utf-8'))
            data["teacher"] = 1
            data["event_id"] = event_id
            answer["data"]["pupils"] = get_pupils(data)
            answer["data"]["lessons"] = get_lessons(data)
            data["pupils"] = answer["data"]["pupils"]
            data["lessons"] = answer["data"]["lessons"]
            answer["data"]["marks"] = get_marks(data)
        except Exception as e:
            print(str(e))
            answer["error"] = "Error: " + str(e)
        return HttpResponse(json.dumps(answer), content_type="application/json")
    else:
        return HttpResponseNotFound(request)


def update_homework_teacher(request, event_id):
    if request.method == "POST" and request.is_ajax:
        answer = dict()
        answer["data"] = list()
        try:
            data = json.loads(request.body.decode('utf-8'))
            if data['id'] == "":
                #new homework
                homework = Homework(title=data["task"])
                homework.comment = data["comment"] if data["comment"] != "" else None
                homework.to_lesson = Lesson.objects.get(id=int(data["lesson_id"]))
                homework.from_lesson = Lesson.objects.get(id=int(data["lesson_id"])) #Temp
                homework.save()
            else:
                homework = Homework.objects.get(id=int(data['id']))
                homework.title = data["task"]
                homework.comment = data["comment"] if data["comment"] != "" else None
                homework.save()
        except Exception as e:
            print(str(e))
            answer["error"] = "Error: " + str(e)
        return HttpResponse(json.dumps(answer), content_type="application/json")
    else:
        return HttpResponseNotFound(request)


def update_lesson_teacher(request, event_id):
    if request.method == "POST" and request.is_ajax:
        answer = dict()
        answer["data"] = list()
        try:
            data = json.loads(request.body.decode('utf-8'))
            lesson = Lesson.objects.get(id=data['id'], event__id=event_id)
            lesson.title = data["title"]
            lesson.comment = data["comment"] if data["comment"] != "" else None
            lesson.save()
        except Exception as e:
            print(str(e))
            answer["error"] = "Error: " + str(e)
        return HttpResponse(json.dumps(answer), content_type="application/json")
    else:
        return HttpResponseNotFound(request)


def get_groups_teacher(request, event_id):
    if request.method == "POST" and request.is_ajax:
        answer = dict()
        answer["data"] = dict()
        try:
            data = json.loads(request.body.decode('utf-8'))
            data["event_id"] = event_id
            data["teacher"] = 1
            answer["data"]["groups"] = get_groups(data)
        except Exception as e:
            print(str(e))
            answer["error"] = "Error: " + str(e)
        return HttpResponse(json.dumps(answer), content_type="application/json")
    else:
        return HttpResponseNotFound(request)


def get_lessons_teacher(request, event_id):
    if request.method == "POST" and request.is_ajax:
        answer = dict()
        answer["data"] = dict()
        try:
            data = json.loads(request.body.decode('utf-8'))
            data["event_id"] = event_id
            data["teacher"] = 1
            answer["data"]["lessons"] = get_lessons(data)
        except Exception as e:
            print(str(e))
            answer["error"] = "Error: " + str(e)
        return HttpResponse(json.dumps(answer), content_type="application/json")
    else:
        return HttpResponseNotFound(request)


def get_lessons_admin(request, event_id):
    if request.method == "POST" and request.is_ajax:
        answer = dict()
        answer["data"] = list()
        try:
            data = json.loads(request.body.decode('utf-8'))
            dates = get_date_in_range(datetime.strptime(data["start_date"], '%d/%m/%Y').date(),
                                      datetime.strptime(data["end_date"], '%d/%m/%Y').date(),
                                      1)
            lessons = Lesson.objects.filter(group__id=int(data["group"]), date__in=dates, event__id=event_id).order_by("date", "start_time")
            for lesson in lessons:
                answer["data"].append(dict())
                answer["data"][-1]["id"] = lesson.id
                answer["data"][-1]["date"] = lesson.date.strftime('%d/%m/%Y')
                answer["data"][-1]["start_time"] = lesson.start_time.strftime('%H:%M')
                answer["data"][-1]["end_time"] = lesson.end_time.strftime('%H:%M')
                answer["data"][-1]["group"] = lesson.group.label
                answer["data"][-1]["teacher"] = str(lesson.teacher.data)
                answer["data"][-1]["subject"] = lesson.subject.name
                answer["data"][-1]["place"] = lesson.place
        except Exception as e:
            print(str(e))
            answer["error"] = "Error: " + str(e)
        return HttpResponse(json.dumps(answer), content_type="application/json")
    else:
        return HttpResponseNotFound(request)


def delete_lesson_admin(request, event_id):
    if request.method == "POST" and request.is_ajax:
        answer = dict()
        try:
            data = json.loads(request.body.decode('utf-8'))
            lesson = Lesson.objects.get(id=data, event__id=event_id)
            lesson.delete()
        except Exception as e:
            print(str(e))
            answer["error"] = "Error: " + str(e)
        return HttpResponse(json.dumps(answer), content_type="application/json")
    else:
        return HttpResponseNotFound(request)


def update_lesson_admin(request, event_id):
    if request.method == "POST" and request.is_ajax:
        answer = dict()
        answer["data"] = list()
        try:
            data = json.loads(request.body.decode('utf-8'))
            lesson = Lesson.objects.get(id=data['id'], event__id=event_id)
            lesson.subject = Subject.objects.get(id=int(data['subject']))
            lesson.teacher = Teacher.objects.get(id=int(data['teacher']))
            lesson.start_time = datetime.strptime(data['start_time'], '%H:%M').time()
            lesson.end_time = datetime.strptime(data['end_time'], '%H:%M').time()
            lesson.place = data['place']
            lesson.date = datetime.strptime(data["date"], '%d/%m/%Y').date()
            lesson.save()
        except Exception as e:
            print(str(e))
            answer["error"] = "Error: " + str(e)
        return HttpResponse(json.dumps(answer), content_type="application/json")
    else:
        return HttpResponseNotFound(request)


def add_lessons_admin(request, event_id):
    if request.method == "POST" and request.is_ajax:
        answer = dict()
        answer["data"] = list()
        try:
            data = json.loads(request.body.decode('utf-8'))
            lesson = Lesson(title="Тема не задана")
            lesson.subject = Subject.objects.get(id=int(data['subject']))
            lesson.teacher = Teacher.objects.get(id=int(data['teacher']))
            lesson.group = StudyGroup.objects.get(id=int(data['group']))
            lesson.start_time = datetime.strptime(data['start_time'], '%H:%M').time()
            lesson.end_time = datetime.strptime(data['end_time'], '%H:%M').time()
            lesson.place = data['place']
            lesson.event = Event.objects.get(id=event_id)
            dates = list()
            if data['repeat']:
                if data['until'] == "1":
                    dates = get_date_in_range(datetime.strptime(data["date"], '%d/%m/%Y').date(),
                                              lesson.event.end_date,
                                              int(data["delta"]))
                else:
                    dates = get_date_count(datetime.strptime(data["date"], '%d/%m/%Y').date(),
                                           int(data["times"]),
                                           int(data["delta"]))
            else:
                dates.append(datetime.strptime(data["date"], '%d/%m/%Y').date())
            for cur_date in dates:
                current_lesson = lesson
                current_lesson.id = None
                current_lesson.date = cur_date
                current_lesson.save()
        except Exception as e:
            print(str(e))
            answer["error"] = "Error: " + str(e)
        return HttpResponse(json.dumps(answer), content_type="application/json")
    else:
        return HttpResponseNotFound(request)

#############
##  VIEWS  ##
#############


def as_teacher_left(request, event_id):
    if request.method == "GET":
        subjects = Subject.objects.filter(lesson__teacher__id=1).distinct()
        if len(subjects) == 0:
            return HttpResponseNotFound(request)
        groups = StudyGroup.objects.filter(event__id=event_id,
                                           lesson__teacher__id=1,
                                           lesson__subject=subjects[0]).distinct()
        event = Event.objects.get(id=event_id)
        start_date = event.opened.strftime('%d/%m/%Y')
        end_date = event.closed.strftime('%d/%m/%Y')
        return render(request, 'journal/schedule_teacher_left.html', {'event_id': event_id,
                                                                       'start_date': start_date,
                                                                       'end_date': end_date,
                                                                       'subjects': subjects,
                                                                       'groups': groups})
    else:
        return HttpResponseNotFound(request)


def as_teacher_right(request, event_id):
    if request.method == "GET":
        subjects = Subject.objects.filter(lesson__teacher__id=1).distinct()
        if len(subjects) == 0:
            return HttpResponseNotFound(request)
        groups = StudyGroup.objects.filter(event__id=event_id,
                                           lesson__teacher__id=1,
                                           lesson__subject=subjects[0]).distinct()
        event = Event.objects.get(id=event_id)
        start_date = event.opened.strftime('%d/%m/%Y')
        end_date = event.closed.strftime('%d/%m/%Y')
        return render(request, 'journal/schedule_teacher_right.html', {'event_id': event_id,
                                                                       'start_date': start_date,
                                                                       'end_date': end_date,
                                                                       'subjects': subjects,
                                                                       'groups': groups})
    else:
        return HttpResponseNotFound(request)


def as_admin(request, event_id):
    if request.method == "GET":
        groups = StudyGroup.objects.filter(event__id=event_id)
        subjects = Subject.objects.filter(event__id=event_id)
        teachers = Teacher.objects.filter(event__id=event_id)
        event = Event.objects.get(id=event_id)
        start_date = event.opened.strftime('%d/%m/%Y')
        end_date = event.closed.strftime('%d/%m/%Y')
        repeats = (event.closed - event.opened).days + 1
        return render(request, 'journal/schedule_admin.html', {'groups': groups,
                                                               'event_id': event_id,
                                                               'start_date': start_date,
                                                               'end_date': end_date,
                                                               'subjects': subjects,
                                                               'teachers': teachers,
                                                               'repeats': range(1, repeats + 1)})
    else:
        return HttpResponseNotFound(request)