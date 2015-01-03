# -*- coding: utf-8 -*-

from __future__ import unicode_literals 
from django.forms import ModelForm
from schools.models import School
from django.core.exceptions import ValidationError
import re

class SchoolForm(ModelForm):
    def clean(self):
        cleaned_data = super(SchoolForm, self).clean()
        #should be smart validation
        school_exists = False
        if school_exists:
            if (school_exists.city == cleaned_data['city'] and
               school_exists.country == cleaned_data['country']):
                    raise ValidationError('Такая школа уже существует: %s' %
                                          school_exists.name)

        return cleaned_data

    class Meta:
        model = School
        exclude = ['approved']
