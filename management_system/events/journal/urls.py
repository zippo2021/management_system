from django.conf.urls import patterns, url

from events.journal import schedule

urlpatterns = patterns('',
    url(r'^schedule/as_admin$', schedule.as_admin, name='as_admin'),
    url(r'^schedule/as_teacher/right$', schedule.as_teacher_right, name='as_teacher_right'),
    url(r'^schedule/as_teacher/left$', schedule.as_teacher_left, name='as_teacher_left'),

    url(r'^schedule/get_lessons_admin$', schedule.get_lessons_admin, name='get_lessons_admin'),
    url(r'^schedule/add_lessons_admin$', schedule.add_lessons_admin, name='add_lessons_admin'),
    url(r'^schedule/del_lesson_admin$', schedule.delete_lesson_admin, name='del_lesson_admin'),
    url(r'^schedule/update_lesson_admin$', schedule.update_lesson_admin, name='update_lesson_admin'),

    url(r'^schedule/get_groups_teacher$', schedule.get_groups_teacher, name='get_groups_teacher'),
    url(r'^schedule/get_lessons_teacher$', schedule.get_lessons_teacher, name='get_lessons_teacher'),
    url(r'^schedule/update_lesson_teacher$', schedule.update_lesson_teacher, name='update_lesson_teacher'),
    url(r'^schedule/update_homework_teacher$', schedule.update_homework_teacher, name='update_homework_teacher'),
    url(r'^schedule/get_pupils_lessons_marks', schedule.get_pupils_lessons_marks, name='get_pupils_lessons_marks'),
    url(r'^schedule/set_mark$', schedule.set_mark, name='set_mark'),
)