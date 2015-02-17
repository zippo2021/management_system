#-*- coding: utf-8 *-*
from django.shortcuts import render,redirect
from events.events_admin.models import Event, Requests, Result
from events.study_groups.models import StudyGroup
from events.price_groups.models import PriceGroup
from django.contrib.auth.models import User
from dashboard.teacher.models import Teacher
from dashboard.regular.models import RegularUser
from dashboard.mentor.models import Mentor
from dashboard.observer.models import Observer
from events.events_manage.forms import PriceChoice, ResultForm
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from decorators import should_be_event_worker,should_be_regular
from django.contrib.auth.decorators import login_required

trans = {'Teacher':'teachers','Observer':'observers','Mentor':'mentors'}

@login_required
@should_be_event_worker
def edit_or_create_result(request, event_id, user_id):
    user = RegularUser.objects.get(id = user_id)
    event = Event.objects.get(id = event_id)
    result, created = Result.objects.get_or_create(event = event, user = user)
    if request.method == 'POST':
        form = ResultForm(request.POST, instance = result)
        if form.is_valid():
            result = form.save()
            #FIXME: bad completed page
            return redirect('event_added')
    else:
        form = ResultForm(instance = result)
    return render(request, 'edit_or_create_result.html', {'form' : form})

@login_required
@should_be_event_worker
def main(request,eid):
    event = Event.objects.get(id = eid)
    context = {'name':event.name, 'eid':eid}
    return render(request,'events_manage_main.html',context)

@login_required
@should_be_event_worker
def show_users(request,eid,role):
    event = Event.objects.get(id = eid)
    users = globals()[role].objects.filter(~Q(event=eid),is_active = True)
    context = {'ename':event.name,'eid':eid,'users':users,'role':role}
    return render(request,'users_list.html',context)

@login_required
@should_be_event_worker
def invite(request,eid,uid,role):           
    event = Event.objects.get(id = eid)
    user = User.objects.get(id = uid)
    spec = getattr(user.UserData,role)
    field = getattr(event,trans[role])
    field.add(spec)   
    return redirect('events_show_users',role = role,eid = eid)

@login_required
@should_be_event_worker
def show_requests(request,eid):
    event = Event.objects.get(id = eid)
    requests = Requests.objects.get(event = eid)
    if event.PriceGroup.all():
        accept = True
    else:
        accept = False
    context = {'ename':event.name,'eid':eid,'users':requests.users.all(),'accept':accept}
    return render(request,'requests.html',context)

@login_required
@should_be_event_worker
def accept(request,eid,uid):
    event = Event.objects.get(id = eid)
    if request.method == "POST":
        form = PriceChoice(request.POST,event_id=eid)
        if form.is_valid():
            user = User.objects.get(id = uid)
            spec = user.UserData.RegularUser
            s_group = event.StudyGroup.objects.get(label='All')
            s_group.users.add(spec)
            p_group = form.cleaned_data.PriceGroup
            p_group.users.add(spec)
            return redirect('events_show_requests',eid = eid)
    else:
        form = PriceChoice(event_id=eid) 
    return render(request,'price_choice_form.html',{'form':form,'eid':eid})

def deny_request(request,eid,uid):
    event = Event.objects.get(id = eid)
    #FIXME обсудить про отказ и статус
    
@login_required
@should_be_regular
def place_request(request,eid):
    event = Event.objects.get(id = eid)
    try:
        e_request = event.Requests.get()
    except ObjectDoesNotExist:
        e_request = Requests(event = eid)
        e_request.save()
    e_request.users.add(request.user.UserData.RegularUser)
    return redirect('request_completed',eid=eid )

@login_required
@should_be_regular
def request_completed(request,eid):
    return render(request,'request_completed.html')

    
    
    
