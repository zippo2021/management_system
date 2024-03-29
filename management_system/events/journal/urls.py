

from django.conf.urls import patterns, url

from events.journal import schedule

urlpatterns = patterns('',
    url(r'^journal$', schedule.index, name='journal_index'),
    url(r'^journal/schedule$', schedule.schedule_index, name='journal_schedule_index'),

    url(r'^journal/admin$', schedule.as_admin, name='journal_admin'),
    url(r'^journal/admin/subjects$', schedule.subjects, name='journal_subjects'),

    url(r'^journal/teacher/right$', schedule.as_teacher_right, name='journal_teacher_right'),
    url(r'^journal/teacher/left$', schedule.as_teacher_left, name='journal_teacher_left'),
    url(r'^journal/teacher/schedule$', schedule.as_teacher_schedule, name='journal_teacher_schedule'),

    url(r'^journal/pupil/schedule$', schedule.as_pupil_schedule, name='journal_pupil_schedule'),
    url(r'^journal/pupil/marks$', schedule.as_pupil_marks, name='journal_pupil_marks'),

    url(r'^journal/admin/get_lessons$', schedule.get_lessons_admin, name='journal_admin_get_lessons'),
    url(r'^journal/admin/add_lessons$', schedule.add_lessons_admin, name='journal_admin_add_lessons'),
    url(r'^journal/admin/del_lesson$', schedule.delete_lesson_admin, name='journal_admin_del_lesson'),
    url(r'^journal/admin/update_lesson$', schedule.update_lesson_admin, name='journal_admin_update_lesson'),
    url(r'^journal/admin/delete_subject$', schedule.delete_subject_admin, name='journal_admin_delete_subject'),
    url(r'^journal/admin/add_subject$', schedule.add_subject_admin, name='journal_admin_add_subject'),
    url(r'^journal/admin/get_subjects$', schedule.get_subjects_admin, name='journal_admin_get_subjects'),

    url(r'^journal/teacher/get_groups$', schedule.get_groups_teacher, name='journal_teacher_get_groups'),
    url(r'^journal/teacher/get_lessons$', schedule.get_lessons_teacher, name='journal_teacher_get_lessons'),
    url(r'^journal/teacher/update_lesson$', schedule.update_lesson_teacher, name='journal_teacher_update_lesson'),
    url(r'^journal/teacher/update_homework$', schedule.update_homework_teacher, name='journal_teacher_update_homework'),
    url(r'^journal/teacher/get_pupils_lessons_marks', schedule.get_pupils_lessons_marks, name='journal_teacher_get_pupils_lessons_marks'),
    url(r'^journal/teacher/set_mark$', schedule.set_mark, name='journal_teacher_set_mark'),
    url(r'^journal/teacher/get_schedule$', schedule.get_schedule_teacher, name='journal_teacher_get_schedule'),

    url(r'^journal/pupil/get_schedule$', schedule.get_schedule_pupil, name='journal_pupil_get_schedule'),
    url(r'^journal/pupil/get_marks$', schedule.get_marks_pupil, name='journal_pupil_get_marks'),
)
