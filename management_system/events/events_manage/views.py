from django.shortcuts import render,redirect
from events.events_admin.models import Event,Requests
from events.study_groups.models import StudyGroup
from events.price_groups.models import PriceGroup
from django.contrib.auth.models import User
from dashboard.teacher.models import Teacher
from dashboard.regular.models import RegularUser
from dashboard.mentor.models import Mentor
from dashboard.observer.models import Observer
from events.events_manage.forms import PriceChoice
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

trans = {'Teacher':'teachers','Observer':'observers','Mentor':'mentors'}


def main(request,eid):
    event = Event.objects.get(id = eid)
    context = {'name':event.name, 'eid':eid}
    return render(request,'events_manage_main.html',context)

def show_users(request,eid,role):
    event = Event.objects.get(id = eid)
    if role !="RegularUser":
        users = globals()[role].objects.filter(~Q(event=eid),is_active = True)
    else:
        users = globals()[role].objects.filter(~Q(StudyGroup=eid))#FIXME
    context = {'ename':event.name,'eid':eid,'users':users,'role':role}
    return render(request,'users_list.html',context)

def invite(request,eid,uid,role):           
    event = Event.objects.get(id = eid)
    user = User.objects.get(id = uid)
    spec = getattr(user.UserData,role)
    if role !="RegularUser":
        field = getattr(event,trans[role])
        field.add(spec)
    else:
        group = event.StudyGroup.get(label='All')
        group.users.add(spec)
    return redirect('events_show_users',role = role,eid = eid)



def show_requests(request,eid):
    event = Event.objects.get(id = eid)
    requests = Requests.objects.get(event = eid)
    if event.PriceGroup.all():
        accept = True
    else:
        accept = False
    context = {'ename':event.name,'eid':eid,'users':requests,'accept':accept}
    return render(request,'users_list.html',context)

def accept(request,eid,uid,price):
    event = Event.objects.get(id = eid)
    if request.method == "POST":
        form = PriceChoice(request.POST,instance=event)
        if form.is_valid():
            user = User.objects.get(id = uid)
            spec = user.UserData.RegularUser
            s_group = event.StudyGroup.objects.get(label='All')
            s_group.users.add(spec)
            p_group = form.cleaned_data.PriceGroup
            p_group.users.add(spec)
            return redirect('events_show_requests',eid = eid)
    else:
        form = PriceChoice(instance=event) 
        return render(request,'price_choice_form.html',{'form':form,'eid':eid})
    
def place_request(request,eid):
    event = Event.objects.get(id = eid)
    try:
        e_request = event.Requests.get()
    except ObjectDoesNotExist:
        e_request = Requests(event = eid)
        e_request.save()
    e_request.users.add(request.user.UserData.RegularUser)
    return redirect('request_completed',eid=eid )

def request_completed(request,eid):
    return render(request,'request_completed.html')

    
    
    
