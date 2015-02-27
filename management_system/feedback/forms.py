# -*- coding: utf-8 -*-

from django.forms import Form, CharField, ChoiceField, Textarea

class FeedBackForm(Form):
    problem_type = ChoiceField(
        choices = (('T', 'Технический вопрос'),
                   ('A', 'Административный вопрос')),
                   label = 'Тип',
                   required = True)
    subject = CharField(label = 'Тема')
    text = CharField(label = 'Письмо', widget = Textarea)
