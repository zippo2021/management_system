# -*- coding: utf-8 -*-
from dashboard.teacher.models import Teacher
from events.events_admin.models import Event
from dashboard.regular.models import RegularUser
from events.study_groups.models import StudyGroup
from events.journal.models import Lesson, Subject, Homework, Mark
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from decorators import should_be_teacher, should_be_defined, should_be_regular, should_be_event_worker, should_be_allowed_for_event
import json
from django.db import IntegrityError
from django.db.models import Q
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


def check_collisions(lesson):
    #check teacher collision
    lessons = Lesson.objects.filter(teacher=lesson.teacher, date=lesson.date)\
                    .exclude(Q(end_time__lte=lesson.start_time), Q(end_time__lte=lesson.end_time))\
                    .exclude(Q(start_time__gte=lesson.start_time), Q(start_time__gte=lesson.end_time))
    if len(lessons) > 0:
        return False
    #check pupil collisions
    pupils = RegularUser.objects.filter(StudyGroup=lesson.group)
    lessons = Lesson.objects.filter(group__users__in=pupils, date=lesson.date)\
                    .exclude(Q(end_time__lte=lesson.start_time), Q(end_time__lte=lesson.end_time))\
                    .exclude(Q(start_time__gte=lesson.start_time), Q(start_time__gte=lesson.end_time))
    if len(lessons) > 0:
        return False
    return True


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
    pupils = RegularUser.objects.filter(StudyGroup__id=int(data["study_group"]),
                                        Request__event__id=int(data["event_id"]))\
        .order_by("data__last_name").order_by("data__first_name")
    for pupil in pupils:
        answer.append(dict())
        answer[-1]["name"] = str(pupil.data)
        answer[-1]["id"] = pupil.id
    return answer


def get_lessons(data):
    dates = get_date_in_range(datetime.strptime(data["start_date"], '%d.%m.%Y').date(),
                              datetime.strptime(data["end_date"], '%d.%m.%Y').date(),
                              1)
    lessons = Lesson.objects.filter(group__id=int(data["study_group"]),
                                    teacher__id=int(data["teacher"]),
                                    subject__id=int(data['subject']),
                                    date__in=dates,
                                    event__id=int(data["event_id"])).order_by("date", "start_time")
    answer = list()
    for lesson in lessons:
        homeworks = Homework.objects.filter(to_lesson=lesson)
        answer.append(dict())
        answer[-1]["id"] = lesson.id
        answer[-1]["date"] = lesson.date.strftime('%d.%m.%Y')
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


@login_required
@should_be_allowed_for_event
@should_be_regular
def get_marks_pupil(request, event_id):
    if request.method == "POST" and request.is_ajax:
        pupil_id = request.user.UserData.RegularUser.id
        answer = dict()
        answer["data"] = dict()
        try:
            data = json.loads(request.body.decode('utf-8'))
            dates = get_date_in_range(datetime.strptime(data["start_date"], '%d.%m.%Y').date(),
                                      datetime.strptime(data["end_date"], '%d.%m.%Y').date(),
                                      1)
            lessons = Lesson.objects.filter(event__id=event_id, group__users=pupil_id, date__in=dates)\
                .distinct().order_by('date').order_by('start_time')
            marks = Mark.objects.filter(lesson__in=lessons, pupil__id=pupil_id).distinct()
            subjects = Subject.objects.filter(event__id=event_id, lesson__in=lessons).distinct().order_by('name')
            lessons_ids = list(lesson.id for lesson in lessons)
            subjects_ids = list(subject.id for subject in subjects)

            answer["data"]["subjects"] = list()
            for subject in subjects:
                answer["data"]["subjects"].append(dict())
                answer["data"]["subjects"][-1]["id"] = subject.id
                answer["data"]["subjects"][-1]["name"] = subject.name

            answer["data"]["lessons"] = list()
            for lesson in lessons:
                answer["data"]["lessons"].append(dict())
                answer["data"]["lessons"][-1]["id"] = lesson.id
                answer["data"]["lessons"][-1]["title"] = lesson.title
                answer["data"]["lessons"][-1]["date"] = lesson.date.strftime('%d.%m.%Y')

            answer["data"]["marks"] = dict()
            for sid in subjects_ids:
                answer["data"]["marks"][sid] = dict()
                for lid in lessons_ids:
                    answer["data"]["marks"][sid][lid] = ""

            for mark in marks:
                answer["data"]["marks"][mark.lesson.subject.id][mark.lesson.id] = mark.mark

        except Exception as e:
            print(str(e))
            answer["error"] = "Error: " + str(e)
        return HttpResponse(json.dumps(answer), content_type="application/json")
    else:
        return HttpResponseNotFound(request)


@login_required
@should_be_allowed_for_event
@should_be_regular
def get_schedule_pupil(request, event_id):
    if request.method == "POST" and request.is_ajax:
        pupil_id = request.user.UserData.RegularUser.id
        answer = dict()
        answer["data"] = dict()
        try:
            data = json.loads(request.body.decode('utf-8'))
            dates = get_date_in_range(datetime.strptime(data["start_date"], '%d.%m.%Y').date(),
                                      datetime.strptime(data["end_date"], '%d.%m.%Y').date(),
                                      1)
            lessons = Lesson.objects.filter(event__id=event_id, group__users=pupil_id, date__in=dates)\
                .distinct().order_by('date').order_by('start_time')
            prev_date = ""
            for lesson in lessons:
                if lesson.date != prev_date:
                    prev_date = lesson.date.strftime('%d.%m.%Y')
                    answer["data"][prev_date] = list()
                answer["data"][prev_date].append(dict())
                answer["data"][prev_date][-1]["subject"] = str(lesson.subject)
                answer["data"][prev_date][-1]["start_time"] = str(lesson.start_time.strftime('%H:%M'))
                answer["data"][prev_date][-1]["end_time"] = str(lesson.end_time.strftime('%H:%M'))
                answer["data"][prev_date][-1]["study_group"] = str(lesson.group)
                answer["data"][prev_date][-1]["place"] = lesson.place
        except Exception as e:
            print(str(e))
            answer["error"] = "Error: " + str(e)
        return HttpResponse(json.dumps(answer), content_type="application/json")
    else:
        return HttpResponseNotFound(request)


@login_required
@should_be_allowed_for_event
@should_be_teacher
def get_schedule_teacher(request, event_id):
    if request.method == "POST" and request.is_ajax:
        teacher_id = request.user.UserData.Teacher.id
        answer = dict()
        answer["data"] = dict()
        try:
            data = json.loads(request.body.decode('utf-8'))
            dates = get_date_in_range(datetime.strptime(data["start_date"], '%d.%m.%Y').date(),
                                      datetime.strptime(data["end_date"], '%d.%m.%Y').date(),
                                      1)
            lessons = Lesson.objects.filter(event__id=event_id, teacher__id=teacher_id, date__in=dates)\
                .distinct().order_by('date').order_by('start_time')
            prev_date = ""
            for lesson in lessons:
                if lesson.date != prev_date:
                    prev_date = lesson.date.strftime('%d.%m.%Y')
                    answer["data"][prev_date] = list()
                answer["data"][prev_date].append(dict())
                answer["data"][prev_date][-1]["subject"] = str(lesson.subject)
                answer["data"][prev_date][-1]["start_time"] = str(lesson.start_time.strftime('%H:%M'))
                answer["data"][prev_date][-1]["end_time"] = str(lesson.end_time.strftime('%H:%M'))
                answer["data"][prev_date][-1]["study_group"] = str(lesson.group)
                answer["data"][prev_date][-1]["place"] = lesson.place
        except Exception as e:
            print(str(e))
            answer["error"] = "Error: " + str(e)
        return HttpResponse(json.dumps(answer), content_type="application/json")
    else:
        return HttpResponseNotFound(request)


@login_required
@should_be_allowed_for_event
@should_be_teacher
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


@login_required
@should_be_allowed_for_event
@should_be_teacher
def get_pupils_lessons_marks(request, event_id):
    if request.method == "POST" and request.is_ajax:
        teacher_id = request.user.UserData.Teacher.id
        answer = dict()
        answer["data"] = dict()
        try:
            data = json.loads(request.body.decode('utf-8'))
            data["teacher"] = teacher_id
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


@login_required
@should_be_allowed_for_event
@should_be_teacher
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


@login_required
@should_be_allowed_for_event
@should_be_teacher
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


@login_required
@should_be_allowed_for_event
@should_be_teacher
def get_groups_teacher(request, event_id):
    if request.method == "POST" and request.is_ajax:
        teacher_id = request.user.UserData.Teacher.id
        answer = dict()
        answer["data"] = dict()
        try:
            data = json.loads(request.body.decode('utf-8'))
            data["event_id"] = event_id
            data["teacher"] = teacher_id
            answer["data"]["groups"] = get_groups(data)
        except Exception as e:
            print(str(e))
            answer["error"] = "Error: " + str(e)
        return HttpResponse(json.dumps(answer), content_type="application/json")
    else:
        return HttpResponseNotFound(request)


@login_required
@should_be_allowed_for_event
@should_be_teacher
def get_lessons_teacher(request, event_id):
    if request.method == "POST" and request.is_ajax:
        teacher_id = request.user.UserData.Teacher.id
        answer = dict()
        answer["data"] = dict()
        try:
            data = json.loads(request.body.decode('utf-8'))
            data["event_id"] = event_id
            data["teacher"] = teacher_id
            answer["data"]["lessons"] = get_lessons(data)
        except Exception as e:
            print(str(e))
            answer["error"] = "Error: " + str(e)
        return HttpResponse(json.dumps(answer), content_type="application/json")
    else:
        return HttpResponseNotFound(request)


@login_required
@should_be_allowed_for_event
@should_be_event_worker
def get_lessons_admin(request, event_id):
    if request.method == "POST" and request.is_ajax:
        answer = dict()
        answer["data"] = list()
        try:
            data = json.loads(request.body.decode('utf-8'))
            dates = get_date_in_range(datetime.strptime(data["start_date"], '%d.%m.%Y').date(),
                                      datetime.strptime(data["end_date"], '%d.%m.%Y').date(),
                                      1)
            lessons = Lesson.objects.filter(group__id=int(data["group"]), date__in=dates, event__id=event_id).order_by("date", "start_time")
            for lesson in lessons:
                answer["data"].append(dict())
                answer["data"][-1]["id"] = lesson.id
                answer["data"][-1]["date"] = lesson.date.strftime('%d.%m.%Y')
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


@login_required
@should_be_allowed_for_event
@should_be_event_worker
def delete_lesson_admin(request, event_id):
    if request.method == "POST" and request.is_ajax:
        answer = dict()
        try:
            data = json.loads(request.body.decode('utf-8'))
            lesson = Lesson.objects.get(id=data, event__id=event_id)
            lesson.delete()
        except IntegrityError as e:
            answer["error"] = "Нельзя удалить занятие, по которому проставлены оценки"
        except Exception as e:
            print(str(e))
            answer["error"] = "Error: " + str(e)
        return HttpResponse(json.dumps(answer), content_type="application/json")
    else:
        return HttpResponseNotFound(request)


@login_required
@should_be_allowed_for_event
@should_be_event_worker
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
            lesson.date = datetime.strptime(data["date"], '%d.%m.%Y').date()
            lesson.save()
        except Exception as e:
            print(str(e))
            answer["error"] = "Error: " + str(e)
        return HttpResponse(json.dumps(answer), content_type="application/json")
    else:
        return HttpResponseNotFound(request)


@login_required
@should_be_allowed_for_event
@should_be_event_worker
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
                    dates = get_date_in_range(datetime.strptime(data["date"], '%d.%m.%Y').date(),
                                              lesson.event.closed,
                                              int(data["delta"]))
                else:
                    dates = get_date_count(datetime.strptime(data["date"], '%d.%m.%Y').date(),
                                           int(data["times"]),
                                           int(data["delta"]))
            else:
                dates.append(datetime.strptime(data["date"], '%d.%m.%Y').date())
            for cur_date in dates:
                current_lesson = lesson
                current_lesson.id = None
                current_lesson.date = cur_date
                if check_collisions(current_lesson):
                    current_lesson.save()
                else:
                    print('skip lesson')
        except Exception as e:
            print(str(e))
            answer["error"] = "Error: " + str(e)
        return HttpResponse(json.dumps(answer), content_type="application/json")
    else:
        return HttpResponseNotFound(request)


@login_required
@should_be_allowed_for_event
@should_be_event_worker
def delete_subject_admin(request, event_id):
    if request.method == "POST" and request.is_ajax:
        answer = dict()
        try:
            data = json.loads(request.body.decode('utf-8'))
            Subject.objects.get(event__id=event_id, id=data).delete()
        except Exception as e:
            print(str(e))
            answer["error"] = "Error: " + str(e)
        return HttpResponse(json.dumps(answer), content_type="application/json")
    else:
        return HttpResponseNotFound(request)


@login_required
@should_be_allowed_for_event
@should_be_event_worker
def add_subject_admin(request, event_id):
    if request.method == "POST" and request.is_ajax:
        answer = dict()
        try:
            data = json.loads(request.body.decode('utf-8'))
            if data == '':
                raise Exception('Поле не должно быть пустым')
            subjects = Subject.objects.filter(event__id=event_id, name=data)
            if len(subjects) == 0:
                subject = Subject(name=data, event_id=event_id)
                subject.save()
            else:
                answer["error"] = "Subject already exists"
        except Exception as e:
            print(str(e))
            answer["error"] = "Error: " + str(e)
        return HttpResponse(json.dumps(answer), content_type="application/json")
    else:
        return HttpResponseNotFound(request)


@login_required
@should_be_allowed_for_event
@should_be_event_worker
def get_subjects_admin(request, event_id):
    if request.method == "POST" and request.is_ajax:
        answer = dict()
        try:
            subjects = Subject.objects.filter(event__id=event_id)
            answer["data"] = list()
            for subject in subjects:
                answer["data"].append(dict())
                answer["data"][-1]["id"] = subject.id
                answer["data"][-1]["name"] = subject.name
        except Exception as e:
            print(str(e))
            answer["error"] = "Error: " + str(e)
        return HttpResponse(json.dumps(answer), content_type="application/json")
    else:
        return HttpResponseNotFound(request)


#############
##  VIEWS  ##
#############


@login_required
@should_be_defined
@should_be_allowed_for_event
def index(request, event_id):
    if request.user.UserData.Admin.is_active:
        return redirect('journal_admin', event_id=event_id)
    elif request.user.UserData.Teacher.is_active:
        return redirect('journal_teacher_right', event_id=event_id)
    elif request.user.UserData.RegularUser.is_active:
        return redirect('journal_pupil_marks', event_id=event_id)
    else:
        return HttpResponseNotFound(request)


@login_required
@should_be_defined
@should_be_allowed_for_event
def schedule_index(request, event_id):
    if request.user.UserData.Admin.is_active:
        return redirect('journal_admin', event_id=event_id)
    elif request.user.UserData.Teacher.is_active:
        return redirect('journal_teacher_schedule', event_id=event_id)
    elif request.user.UserData.RegularUser.is_active:
        return redirect('journal_pupil_schedule', event_id=event_id)
    else:
        return HttpResponseNotFound(request)


@login_required
@should_be_allowed_for_event
@should_be_regular
def as_pupil_marks(request, event_id):
    if request.method == "GET":
        event = Event.objects.get(id=event_id)
        return render(request, 'journal/journal_pupil_marks.html', {'event': event})
    else:
        return HttpResponseNotFound(request)


@login_required
@should_be_allowed_for_event
@should_be_regular
def as_pupil_schedule(request, event_id):
    if request.method == "GET":
        event = Event.objects.get(id=event_id)
        return render(request, 'journal/journal_pupil_schedule.html', {'event': event})
    else:
        return HttpResponseNotFound(request)


@login_required
@should_be_allowed_for_event
@should_be_teacher
def as_teacher_schedule(request, event_id):
    if request.method == "GET":
        event = Event.objects.get(id=event_id)
        return render(request, 'journal/journal_teacher_schedule.html', {'event': event})
    else:
        return HttpResponseNotFound(request)


@login_required
@should_be_allowed_for_event
@should_be_teacher
def as_teacher_left(request, event_id):
    if request.method == "GET":
        teacher_id = request.user.UserData.Teacher.id
        subjects = Subject.objects.filter(lesson__teacher__id=teacher_id).distinct()
        if len(subjects) == 0:
            return HttpResponseNotFound(request)
        groups = StudyGroup.objects.filter(event__id=event_id,
                                           lesson__teacher__id=teacher_id,
                                           lesson__subject=subjects[0]).distinct()
        event = Event.objects.get(id=event_id)
        return render(request, 'journal/journal_teacher_left.html', {'event': event,
                                                                     'subjects': subjects,
                                                                     'groups': groups})
    else:
        return HttpResponseNotFound(request)


@login_required
@should_be_allowed_for_event
@should_be_teacher
def as_teacher_right(request, event_id):
    if request.method == "GET":
        teacher_id = request.user.UserData.Teacher.id
        subjects = Subject.objects.filter(lesson__teacher__id=teacher_id).distinct()
        if len(subjects) == 0:
            return HttpResponseNotFound(request)
        groups = StudyGroup.objects.filter(event__id=event_id,
                                           lesson__teacher__id=teacher_id,
                                           lesson__subject=subjects[0]).distinct()
        event = Event.objects.get(id=event_id)
        return render(request, 'journal/journal_teacher_right.html', {'event': event,
                                                                      'subjects': subjects,
                                                                      'groups': groups})
    else:
        return HttpResponseNotFound(request)


@login_required
@should_be_allowed_for_event
@should_be_event_worker
def subjects(request, event_id):
    if request.method == "GET":
        event = Event.objects.get(id=event_id)
        return render(request, 'journal/journal_subjects.html', {'event': event})
    else:
        return HttpResponseNotFound(request)


@login_required
@should_be_allowed_for_event
@should_be_event_worker
def as_admin(request, event_id):
    if request.method == "GET":
        groups = StudyGroup.objects.filter(event__id=event_id)
        subjects = Subject.objects.filter(event__id=event_id)
        teachers = Teacher.objects.filter(event__id=event_id)
        event = Event.objects.get(id=event_id)
        return render(request, 'journal/journal_admin.html', {'groups': groups,
                                                              'event': event,
                                                              'subjects': subjects,
                                                              'teachers': teachers})
    else:
        return HttpResponseNotFound(request)