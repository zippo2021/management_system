#-*- coding: utf-8 *-*
from django.shortcuts import render,redirect
from django.template.loader import get_template_from_string
from django.template import Context, Template
from events.events_admin.models import Event, Request, Result, AcceptanceEmailTemplate
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
from decorators import should_be_event_worker,should_be_allowed_for_event, should_be_allowed_to_view_event
from django.contrib.auth.decorators import login_required
from base_source_functions import send_templated_email
import glob
import os
from django.conf import settings


@login_required
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
    return render(request,'events_manage_main.html', context)

@login_required
def choose_users(request,event_id, role):
    event = Event.objects.get(id = event_id)
    users = globals()[perms_to_classes[role]]\
            .objects.filter(~Q(event=event_id),is_active = True)
    context = {'ename':event.name,'event_id':event_id,'users':users,'role':role}
    return render(request,
                  'events_manage_choose_users.html',
                  context)

@login_required
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
def show_requests(request,event_id):
    event = Event.objects.get(id = event_id)
    requests = Request.objects.filter(event = event_id)
    if (event.PriceGroup.all()) or(event.is_payed) :
        accept = True
    else:
        accept = False
    context = {'ename':event.name,'event_id':event_id,'users':requests,'accept':accept}
    return render(request,
                 'events_manage_show_requests.html',
                 context)

@login_required
@should_be_event_worker
def accept_request(request, event_id, request_id):
    current_rq = Request.objects.get(id=request_id)
    user = current_rq.user
    event = current_rq.event  
    event_id = event.id
    if event.is_payed:          
        if request.method == "POST":
            form = PriceChoiceForm(request.POST,event_id=event_id)
            if form.is_valid():
                spec = current_rq.user                
                current_rq.status = 'Accepted'
                p_group = form.cleaned_data['price_group']
                files =  glob.glob(os.path.join(os.path.join(settings.EVENT_ATTACHMENTS_DIR,str(event_id)), '*'))
                try:
                    template_file = Template(get_template_from_string(AcceptanceEmailTemplate.objects.get(event = event).text))
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
                    pass
                current_rq.save()
                #s_group = StudyGroup.objects.get(event=,label='All')
                #s_group.users.add(spec)
                p_group.users.add(spec)                       
                return redirect('events_manage_show_requests',
                                event_id = event_id)
        else:
            form = PriceChoiceForm(event_id=event_id) 
        return render(request,
                      'price_choice_form.html',
                      {'form':form,'event_id':event_id})
    else:
        spec = user
        current_rq = Request.objects.get(event=event,user=spec)
        template_file = Template(get_template_from_string(AcceptanceEmailTemplate.objects.get(event = event).text))
        current_rq.status = 'Accepted'
        files =  glob.glob(os.path.join(os.path.join(settings.EVENT_ATTACHMENTS_DIR,str(event_id)), '*'))
        send_templated_email(
                            subject='Подтверждение заявки',
                            template_file=template_file,
                            email_context={
                            'event': event.name,                        
                            },
		    				recipients=user.data.user.email,
                            fail_silently=False,
		    				files=files,
                )
        current_rq.save()
        return redirect('events_manage_show_requests',
                        event_id = event_id)
        

@login_required
def decline_request(request, event_id, request_id):    
    current_rq = Request.objects.get(id=request_id)
    event = current_rq.event
    current_rq.status = 'Declined'
    current_rq.save() 
    return redirect('events_manage_show_requests',event_id=event.id)
    
@login_required
def place_request(request, event_id):
    event = Event.objects.get(id = event_id)
    e_request, created = Request.objects.get_or_create(event = event, user = request.user.UserData.RegularUser)
    if created:
        e_request.status = 'Processing'
        e_request.save()
    else:
        pass #FIXME
    return redirect('completed')

@login_required
def create_acceptance_email_template(request,event_id):
    event = Event.objects.get(id = event_id)
    template, created = AcceptanceEmailTemplate.objects.\
                            get_or_create(event = event)
    if request.method == "POST":
        form = AcceptanceEmailTemplateForm(request.POST, instance = template)
        if form.is_valid():
            form.save()
            return redirect('completed')
    else:
        form = AcceptanceEmailTemplateForm(instance = template)
    return render(request,
                  'events_manage_create_acceptance_email_form.html',
                  {'form':form})

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
