from django.shortcuts import render,redirect
from events.events_admin.models import Event
from events.study_groups.models import StudyGroup
from django.contrib.auth.models import User

trans = {'Teacher':'teachers','Observer':'observers','Mentor':'mentors'}


def main(request,eid):
    event = Event.objects.get(id = eid)
    context = {'name':event.name, 'eid':eid}
    return render('events_manage_main.html',context)

def show_users(request,eid,role):
    event = Event.objects.get(id = eid)
    if role != 'RegularUser':
        users = getattr(event,trans[role]).objects.all()
    else:
        group = Event.objects.get(event = event)
        users =  group.users.objects.all()
    context = {'ename':event.name,'eid':eid,'users':users,'role':role}
    return render('users_list.html',context)

def invite(request,eid,uid,role):           #for everyone except RegularUser
    event = Event.objects.get(id = eid)
    user = User.objects.get(id = uid)
    spec = getattr(user.UserData,role)
    field = getattr(event,trans[role])
    field.add(spec)    
    return redirect('event_show_users',role = role,eid = eid)

    
    
    
