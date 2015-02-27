#-*- coding: utf-8 *-*
from django.shortcuts import render,redirect
from django.template.loader import get_template_from_string
from django.template import Context, Template
from events.events_admin.models import Event
from events.events_manage.models import Request, Result, EmailTemplate
from events.study_groups.models import StudyGroup
from events.price_groups.models import PriceGroup
from django.contrib.auth.models import User
from dashboard.teacher.models import Teacher
from dashboard.regular.models import RegularUser
from dashboard.mentor.models import Mentor
from dashboard.observer.models import Observer
from events.events_manage.forms import PriceChoiceForm, ResultForm, AcceptanceEmailTemplateForm
from user_manager.permissions import perms_to_classes
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from decorators import should_be_event_worker, should_be_allowed_for_event,\
should_be_allowed_to_view_event, should_have_filled_data,\
should_be_regular, should_be_allowed_to_view_event
from django.contrib.auth.decorators import login_required
from base_source_functions import send_templated_email
import glob
import os
from django.conf import settings
from django.http import HttpResponse

############################################################
##################### RRESULTS ############################
##########################################################

@login_required
@should_be_event_worker
@should_be_allowed_to_view_event
def show_results(request, event_id):
    event = Event.objects.get(id = event_id)
    requests = Request.objects.filter(event = event, status = 'одобрена')
    users = [each.user for each in requests]
    users_and_results = {}
    for each in users:
        try:
            result = Result.objects.get(user = user, event = event)
            users_and_results.update({each : result})
        except:
            users_and_results.update({each : None})
    return render(request,
                  'events_manage_show_results.html',
                  {'users_and_results' : users_and_results, 'event' : event})

@login_required
@should_be_event_worker
@should_be_allowed_for_event
def edit_or_create_result(request, event_id, user_id):
    user = RegularUser.objects.get(id = user_id)
    event = Event.objects.get(id = event_id)
    result, created = Result.objects.get_or_create(event = event, user = user)
    if request.method == 'POST':
        form = ResultForm(request.POST, instance = result)
        if form.is_valid():
            result = form.save()
            return redirect('completed')
    else:
        form = ResultForm(instance = result)
    return render(request,
                  'events_manage_edit_or_create_result.html',
                  {'form' : form})

@login_required
@should_be_allowed_to_view_event
def main(request,event_id):
    event = Event.objects.get(id = event_id)
    context = {'event' : event}
    try:
        rq = Request.objects.get(user = request.user.UserData.RegularUser,
                                      event = event)
        context.update({'rq' : rq})
    except:
        pass
    return render(request,'events_manage_main.html', context)

###############################################################
####################### STAFF ################################
#############################################################

@login_required
@should_be_event_worker
@should_be_allowed_for_event
def choose_users(request,event_id, role):
    event = Event.objects.get(id = event_id)
    free_users = globals()[perms_to_classes[role]]\
            .objects.filter(~Q(event=event_id),is_active = True,
                            data__modified = True)
    not_free_users = globals()[perms_to_classes[role]]\
            .objects.filter(event=event_id)
    context = {'event' : event, 'free_users' : free_users,
               'not_free_users' : not_free_users, 'role':role}
    return render(request,
                  'events_manage_choose_users.html',
                  context)

@login_required
@should_be_event_worker
@should_be_allowed_for_event
def invite(request,event_id, uid, role):           
    event = Event.objects.get(id = event_id)
    user = User.objects.get(id = uid)
    spec = getattr(user.UserData, perms_to_classes[role])
    field = getattr(event, role + 's')
    field.add(spec)   
    return redirect('events_manage_choose_users',
                    role = role,
                    event_id = event_id)

@login_required
@should_be_event_worker
@should_be_allowed_for_event
def exclude(request, event_id, uid, role):
    event = Event.objects.get(id = event_id)
    user = User.objects.get(id = uid)
    spec = getattr(user.UserData, perms_to_classes[role])
    field = getattr(event, role + 's')
    field.remove(spec)   
    return redirect('events_manage_choose_users',
                    role = role,
                    event_id = event_id)

################################################################
###################### REQUESTS ###############################
##############################################################

@login_required
@should_be_event_worker
@should_be_allowed_for_event
def show_requests(request,event_id):
    event = Event.objects.get(id = event_id)
    requests = Request.objects.filter(event = event_id)
    price_groups = event.PriceGroup.all().order_by('price')
    if event.is_private:
        accept = True
    else:
        accept = False
    context = {'event' : event,
               'users':requests,
               'accept' : accept,
               'price_groups' : price_groups}
    return render(request,
                 'events_manage_show_requests.html',
                 context)

@login_required
@should_be_event_worker
@should_be_allowed_for_event
def accept_request(request, event_id, request_id):
    current_rq = Request.objects.get(id=request_id)
    user = current_rq.user
    event = current_rq.event  
    event_id = event.id
    if request.method == "POST":
        form = PriceChoiceForm(request.POST,event_id=event_id)
        if form.is_valid():
            spec = current_rq.user                
            current_rq.status = 'одобрена'
            p_group = form.cleaned_data['price_group']
            files =  glob.glob(os.path.join(os.path.join(settings.EVENT_ATTACHMENTS_DIR,str(event_id)), '*'))
            try:
                template_file = Template(get_template_from_string(EmailTemplate.objects.get(event = event).text))
                print template_file.render({})
                send_templated_email(
                        subject='Подтверждение заявки',
                        template_file = template_file,
                        email_context={
                        'event': event.name,
                        'price': p_group.price,                        
                        },
	        			recipients=user.data.user.email,
                        fail_silently=False,
		            	files=files,
                )
            except ObjectDoesNotExist:
                pass #FIXME
            current_rq.price_group = p_group
            current_rq.save()
            status = "success"
            return HttpResponse(status)
    else:
        form = PriceChoiceForm(event_id=event_id) 
   
    return render(request,
                  'events_manage_price_choice_form.html',
                  {'form':form, 'event':event})

@login_required
@should_be_event_worker
@should_be_allowed_for_event
def decline_request(request, event_id, request_id):    
    current_rq = Request.objects.get(id=request_id)
    event = current_rq.event
    current_rq.status = 'отклонена'
    current_rq.save() 
    return redirect('events_manage_show_requests', event_id = event.id)

@login_required
@should_be_event_worker
@should_be_allowed_for_event
def pop_back_request(request, event_id, request_id):
    current_rq = Request.objects.get(id=request_id)
    event = current_rq.event
    current_rq.status = 'в обработке'
    current_rq.save() 
    return redirect('events_manage_show_requests', event_id = event.id)
    
@login_required
@should_be_regular
@should_be_allowed_to_view_event
def place_request(request, event_id):
    event = Event.objects.get(id = event_id)
    e_request, created = Request.objects.get_or_create(event = event, user = request.user.UserData.RegularUser)
    if created:
        e_request.status = 'в обработке'
        e_request.save()
    else:
        pass #FIXME
    return redirect('events_manage_main', event.id)

@login_required
@should_be_regular
@should_be_allowed_to_view_event
def undo_request(request, event_id, request_id):
    event = Event.objects.get(id = event_id)
    e_request = Request.objects.get(id = request_id)
    if e_request.status.encode('utf-8')== 'в обработке':
        e_request.delete()
    return redirect('events_manage_main', event_id)

###############################################################
###################### EMAILS ################################
#############################################################

@login_required
@should_be_allowed_for_event
@should_be_event_worker
def create_acceptance_email_template(request,event_id):
    event = Event.objects.get(id = event_id)
    template, created = EmailTemplate.objects.\
                            get_or_create(event = event)
    if request.method == "POST":
        form = AcceptanceEmailTemplateForm(request.POST, instance = template)
        if form.is_valid():
            form.save()
            status = "success"
            return HttpResponse(status)
    else:
        form = AcceptanceEmailTemplateForm(instance = template)
    return render(request,
                  'events_manage_create_acceptance_email_form.html',
                  {'form':form, 'event' : event})

'''
@login_required
@should_be_event_worker
def send_email_to_schools(request,event_id):
    event = Event.objects.get(id = event_id)
    users = User.objects.filter(event = event, status = 'Accepted')
    for each in users:
        user = each.user
        send_templated_email(
                            subject='Подтверждение заявки',
                            email_template_name='',
                            email_context={
                            'event': event.name,                        
                            },
		    				recipients=user.email,
                            fail_silently=False,
		    				files=files,
                )
    return render(request,'acceptance_email_form.html',{'form':form})
'''
