from django.contrib import admin
from events.journal.models import Lesson, Homework, Subject, Mark

# Register your models here.
admin.site.register(Subject)
admin.site.register(Lesson)
admin.site.register(Homework)
admin.site.register(Mark)