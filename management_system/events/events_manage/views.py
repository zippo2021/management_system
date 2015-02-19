from django.shortcuts import render,redirect
from events.events_admin.models import Event,Requests,Request
from events.study_groups.models import StudyGroup
from events.price_groups.models import PriceGroup
from django.contrib.auth.models import User
from dashboard.teacher.models import Teacher
from dashboard.regular.models import RegularUser
from dashboard.mentor.models import Mentor
from dashboard.observer.models import Observer
from events.events_manage.forms import PriceChoiceForm
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from decorators import should_be_event_worker,should_be_regular
from django.contrib.auth.decorators import login_required
trans = {'Teacher':'teachers','Observer':'observers','Mentor':'mentors'}

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
        form = PriceChoiceForm(request.POST,event_id=eid)
        if form.is_valid():
            user = User.objects.get(id = uid)
            spec = user.UserData.RegularUser
            current_rq = event.Request.objects.get(user=spec)
            current_rq.status = 'Accepted'
            current_rq.save()
            s_group = event.StudyGroup.objects.get(label='All')
            s_group.users.add(spec)
            p_group = form.cleaned_data.PriceGroup
            p_group.users.add(spec)            
            return redirect('events_show_requests',eid = eid)
    else:
        form = PriceChoice(event_id=eid) 
    return render(request,'price_choice_form.html',{'form':form,'eid':eid})


@login_required
def deny_request(request,eid,uid):
    event = Event.objects.get(id = eid)
    user = User.objects.get(id = uid)
    current_rq = event.Request.objects.get(user=user.UserData.RegularUser)
    current_rq.status = 'Declined'
    current_rq.save() 
    return redirect('events_show_requests',eid=eid)
    
@login_required
@should_be_regular
def place_request(request,eid):
    e_request = Request(event = eid, user = request.user.UserData.RegularUser,status = 'Processing')
    e_request.save()
    return redirect('request_completed',eid=eid )

@login_required
@should_be_regular
def request_completed(request,eid):
    return render(request,'request_completed.html')

    
    
    
