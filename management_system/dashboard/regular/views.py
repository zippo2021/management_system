#-*- coding: utf-8 *-*
from django.shortcuts import render, redirect
from dashboard.regular.models import RegularUser
from dashboard.userdata.models import UserData
from dashboard.regular.forms import RegularUserForm, RegularUserFormStep1, RegularUserFormStep2, RegularUserFormStep3
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from decorators import  should_be_regular, should_be_defined,should_be_staff
from django.core.exceptions import ObjectDoesNotExist
from decorators import should_be_regular_possibly_unfilled, should_be_regular
from django.http import HttpResponse
from django.contrib.formtools.wizard.views import SessionWizardView
from management_system.settings import BASE_DIR


'''
Wizard:
it includes Wizard class with .done() and special wrapper function,
which imitates view function (also loads instances and forms)
so you can access wizard as a simple view, named regular_user_wizard
'''
class RegularUserWizard(SessionWizardView):
    template_name = 'regular_user_wizard.html'
    def done(self, form_list, **kwargs):
        '''
        it's a little bit funny, but there is no need to save first
        steps, because they're using one instance (with third step),
        so they update it
        '''
        #regular = form_list[0].save(commit = False)
        #regular = form_list[1].save(commit = False)
        '''
        end of funny moment. The only line that's needed is below.
        '''
        regular = form_list[2].save(commit = False)
        regular.modified = True
        regular.save()
        return HttpResponse('success')

@login_required
@should_be_regular_possibly_unfilled
def regular_user_wizard(request):
    instance = request.user.UserData.RegularUser
    inst_dict = { '0' : instance,
                  '1' : instance,
                  '2' : instance,
                }
    forms = [RegularUserFormStep1,
             RegularUserFormStep2,
             RegularUserFormStep3
            ]
    return RegularUserWizard.as_view(forms, instance_dict = inst_dict)(request)
'''
end of Wizard
'''

def transfer(request):
    import csv
    import os
    from user_manager.source_functions import create_user
    from datetime import datetime
    from django.db import IntegrityError
    from base_source_functions import send_templated_email
    from dashboard.common_profile.source_functions import perms_to_list
    from user_manager.permissions import perms_to_language
    fields = ('Фамилия','Имя','Отчество','e-mail','Дата рождения','Телефон','Город рождения','Город проживания','Улица','Дом','Корпус','Квартира','Индекс','Тип документа','Серия','Номер','Кем выдан','Когда выдан','Действителен до', 'Код подразделения', 'ФИО отца','Телефон отца','ФИО матери','Телефон матери','Год выпуска','Школа','Учитель физики(истории)','Учитель математики(обществознания)','Директор школы')

    with open(os.path.join(BASE_DIR,'db.csv'),'rb') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fields,delimiter=';')
        for row in reader:
            if (len(row['e-mail'])<30) and (len(row['e-mail'])>0):
                try:
                    password = User.objects.make_random_password(length = 8)
                    perms = {
					          			'event_worker' : False,
								        'teacher' : False,
								        'mentor' : False,
								        'observer' : False,
								        'regular' : True,
                                        'admin' : False,
			        }
                    user = create_user(username=row['e-mail'],email=row['e-mail'],password=password,perms=perms)
                    userdata = user.UserData
                    userdata.first_name = row['Имя']
                    userdata.second_name = row['Отчество']
                    userdata.last_name = row['Фамилия'] 
                    userdata.phone = row['Телефон']
                    userdata.save() 
                    regular = userdata.RegularUser
                    regular.birthdate = datetime.strptime(row['Дата рождения'], '%d.%m.%Y').date()
                    regular.birthplace = row['Город рождения']
                    regular.city = row['Город проживания']
                    regular.street = row['Улица']
                    regular.building = row['Дом']
                    regular.housing = row['Корпус']
                    regular.appartment = row['Квартира']
                    regular.postal_code = row['Индекс']
                    regular.parent_1 = row['ФИО отца']
                    regular.parent_1_phone = row['Телефон отца']
                    regular.parent_2 = row['ФИО матери']
                    regular.parent_2_phone = row['Телефон матери']
                    regular.grad_date = row['Год выпуска']
                    regular.modified = False
                    regular.save()
                    send_templated_email(subject = 'Создан аккаунт', 
				    email_template_name = 'regular_create_email.html',
				    email_context = {'username' : user.username,
								 'password' : password,
								 'perms' : perms_to_list(perms),
								 'admin' : user.is_staff,
                                 'perms_to_language' : perms_to_language,
								 },
				    recipients = user.email,
			)
                except IntegrityError:
                    pass
            else:
                pass                      

 
    return HttpResponse('success')
