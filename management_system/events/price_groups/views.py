from django.shortcuts import render, redirect
from events.price_groups.forms import PriceGroupForm
from events.price_groups.models import PriceGroup
from events.events_admin.models import Event
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from decorators import should_be_event_worker, should_be_allowed_for_event
# Create your views here.

@login_required
@should_be_event_worker
@should_be_allowed_for_event
def add(request, event_id):
    event = Event.objects.get(id = event_id)
    if request.method == "POST":
        form = PriceGroupForm(request.POST)
        if form.is_valid():
            pg = PriceGroup(event = event, price = form.cleaned_data['price'])
            pg.save()
            status = "success"
            return HttpResponse(status)
    else:
        form = PriceGroupForm()
    return render(request,"price_group_form.html",
                        {'form':form, 'event':event})

@login_required
@should_be_event_worker
@should_be_allowed_for_event
def show(request, event_id):
    event = Event.objects.get(id = event_id)
    p_groups = event.PriceGroup.all()
    return render(request,'price_group_show.html',{'p_groups':p_groups,
                        'eid':event_id})
    
