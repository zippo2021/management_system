# -*- coding: utf-8 -*-

from django.forms import Form, CharField


class UserSearchForm(Form):
    first_name = CharField(label='Имя', required=False)
    last_name = CharField(label='Фамилия', required=False)
