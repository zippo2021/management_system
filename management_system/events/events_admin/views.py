from django.shortcuts import render, redirect
from events.events_admin.models import Event
from decorators import should_be_admin
from django.contrib.formtools.wizard.views import SessionWizardView
from events.events_admin.forms import EventForm, EventEditForm, JourneyDataForm, EventMailForm
from events.price_groups.forms import PriceGroupForm
from django.contrib.auth.decorators import login_required

'''
Wizard:
it includes Wizard class with .done() and special wrapper function,
which imitates view function (also loads instances and forms)
so you can access wizard as a simple view, named regular_user_wizard
'''
class EventWizard(SessionWizardView):
    template_name = 'events_admin_wizard.html'
        
    def done(self, form_list, **kwargs):
        
        event = form_list[0].save(commit = False)
        event.is_active = True
        event.save()
        if form_list[0].cleaned_data['is_journey'] == True:
            journey = form_list[1].save(commit = False)
            journey.event = event
            journey.save()
        
        return redirect('completed')

def add_journey_data_condition(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    return cleaned_data.get('is_journey', True)


@login_required
@should_be_admin
def event_wizard(request):
    forms = [EventForm,
             JourneyDataForm,
             EventMailForm,
             ]
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
            return redirect('completed')
    else:
        form = form_class(instance = instance)
    
    return render(request, 'events_admin_edit.html', {'form' : form})

@login_required
@should_be_admin
def delete(request, event_id):
    event = Event.objects.get(id = event_id)
    if hasattr(event, 'JourneyData'):
        event.JourneyData.delete()
    event.delete()
    return redirect('events_admin_show_all')

@login_required
@should_be_admin
def deactivate(request, event_id):
    event = Event.objects.get(id = event_id)
    event.is_active = not(event.is_active)
    event.save()
    return redirect('events_admin_show_all')


@login_required
@should_be_admin
def show_all(request):
    events = Event.objects.all()
    return render(request, 'events_admin_show_all.html', { 'events' : events })
