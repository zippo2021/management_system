# -*- coding: utf- -*-
from django.shortcuts import render, redirect
from events.events_admin.models import Event
from decorators import should_be_admin
from django.contrib.formtools.wizard.views import SessionWizardView
from events.events_admin.forms import EventForm, EventEditForm, JourneyDataForm, EventMailForm
from events.price_groups.forms import PriceGroupForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from events.price_groups.models import PriceGroup
from events.events_manage.models import Request
from dashboard.regular.models import RegularUser
'''
Wizard:
it includes Wizard class with .done() and special wrapper function,
which imitates view function (also loads instances and forms)
so you can access wizard as a simple view, named regular_user_wizard
'''
class EventWizard(SessionWizardView):
    template_name = 'events_admin_event_wizard.html'
        
    def done(self, form_list, **kwargs):
        
        event = form_list[0].save(commit = False)
        event.is_active = True
        event.save()
        if form_list[0].cleaned_data['is_journey'] == True:
            journey = form_list[1].save(commit = False)
            journey.event = event
            journey.save()
        
        return redirect('events_manage_main',event_id = event.id)

def add_journey_data_condition(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    return cleaned_data.get('is_journey', True)


@login_required
@should_be_admin
def event_wizard(request):
    forms = [EventForm,
             JourneyDataForm]
    cond_dict = {'1' : add_journey_data_condition,
                }
    return EventWizard.as_view(forms, condition_dict = cond_dict)(request)
'''
end of Wizard
'''

@login_required
@should_be_admin
def edit(request, event_id, base_or_journey):
    event = Event.objects.get(id = event_id)
    if base_or_journey == 'journey':
        instance = event.JourneyData
        form_class = JourneyDataForm
    elif base_or_journey == 'base':
        instance = event
        form_class = EventEditForm
    else:
        pass
        #!FIXIT! raise error
    
    if request.method == 'POST':
        form = form_class(request.POST, instance = instance)
        if form.is_valid():
            obj = form.save()
            status = "success"
            return HttpResponse(status)
    else:
        form = form_class(instance = instance)
    
    return render(request, 'events_admin_edit.html',
                    {'form' : form, 'event' : event})

@login_required
@should_be_admin
def deactivate(request, event_id):
    event = Event.objects.get(id = event_id)
    tmp = event.is_active
    print 'current status',event.is_active
    event.is_active = not(tmp)
    print 'changed status',event.is_active
    event.save()
    return redirect('events_manage_main', event_id)

#test view!
@login_required
@should_be_admin
def show_all(request):
    events = Event.objects.all()
    return render(request, 'events_admin_show_all.html', { 'events' : events })

def import_data(request,event_id):
    import jsonpickle
    from datetime import datetime
    from django.core.exceptions import ObjectDoesNotExist
    from management_system.settings import BASE_DIR
    import os
    with open(os.path.join(BASE_DIR,'old_data_json.py')) as jsonfile:
        data = jsonfile.read()
        obj = jsonpickle.decode(data)
        for key in obj:
            cur_ev = obj[key]['event_data'] 
            ccc_ev = obj[key]               
            event = Event(
                    name = cur_ev['name'], 
                    comment = cur_ev['comment'],
                    place = cur_ev['place'],
                    opened = cur_ev['issued'],
                    closed = cur_ev['closed'],
                    is_private = True,
                    is_journey = True,
                    has_journal = False,
                    is_active = False,                    
            )
            event.save()
            if cur_ev['price_n']!=0:
                price_group1 = PriceGroup(event = event, price = cur_ev['price_n'])
            else:
                price_group1 = PriceGroup.objects.get( event = event,price = 0)
            if cur_ev['price_po_vs']!=0:            
                price_group2 = PriceGroup(event = event, price = cur_ev['price_po_vs'])
            else:
                price_group2 = PriceGroup.objects.get(event = event, price = 0)
            if cur_ev['price_pr_vs']!=0:            
                price_group3 = PriceGroup(event = event, price = cur_ev['price_pr_vs'])
            else:
                price_group3 = PriceGroup.objects.get(event = event, price = 0)
            if cur_ev['price_ko_ms']!=0:            
                price_group4 = PriceGroup(event = event, price = cur_ev['price_ko_ms'])
            else:
                price_group4 = PriceGroup.objects.get( event = event,price = 0)
            if cur_ev['price_n'] ==cur_ev['price_po_vs']:
                price_group1 = price_group2
            if cur_ev['price_n'] ==cur_ev['price_pr_vs']:
                price_group1 = price_group3
            if cur_ev['price_n'] ==cur_ev['price_ko_ms']:
                price_group1 = price_group4
            if cur_ev['price_po_vs'] ==cur_ev['price_pr_vs']:
                price_group2 = price_group3
            if cur_ev['price_po_vs'] ==cur_ev['price_ko_ms']:
                price_group2 = price_group4
            if cur_ev['price_pr_vs'] ==cur_ev['price_ko_ms']:
                price_group3 = price_group4
            price_group1.save()
            price_group2.save()
            price_group3.save()
            price_group4.save()
            for each in ccc_ev['participants_n']:
                try:
                    user = RegularUser.objects.get(data__user__email=each)
                    rq = Request(status='одобрена',event=event,user=user,price_group=price_group1)
                    rq.save()
                except ObjectDoesNotExist:
                    pass
            for each in ccc_ev['participants_pr_vs']:
                try:
                    user = RegularUser.objects.get(data__user__email=each)
                    rq = Request(status='одобрена',event=event,user=user,price_group=price_group2)
                    rq.save()
                except ObjectDoesNotExist:
                    pass
            for each in ccc_ev['participants_po_vs']:
                try:
                    user = RegularUser.objects.get(data__user__email=each)
                    rq = Request(status='одобрена',event=event,user=user,price_group=price_group3)
                    rq.save()
                except ObjectDoesNotExist:
                    pass
            for each in ccc_ev['participants_ko_ms']:
                try:
                    user = RegularUser.objects.get(data__user__email=each)
                    rq = Request(status='одобрена',event=event,user=user,price_group=price_group4)
                    rq.save()
                except ObjectDoesNotExist:
                    pass
            for each in ccc_ev['declined']:
                try:
                    user = RegularUser.objects.get(data__user__email=each)
                    rq = Request(status='отклонена',event=event,user=user,price_group=price_group2)
                    rq.save()
                except ObjectDoesNotExist:
                    pass
    return HttpResponse(obj)
