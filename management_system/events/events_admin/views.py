from django.shortcuts import render, redirect
from events.events_admin.models import Event
from decorators import should_be_admin
from django.contrib.formtools.wizard.views import SessionWizardView
from events.events_admin.forms import EventForm, JourneyDataForm, EventMailForm
from events.price_groups.forms import PriceGroupForm
from django.contrib.auth.decorators import login_required

'''
Wizard:
it includes Wizard class with .done() and special wrapper function,
which imitates view function (also loads instances and forms)
so you can access wizard as a simple view, named regular_user_wizard
'''
class EventWizard(SessionWizardView):
    template_name = 'event_wizard.html'
        
    def process_step(self, form):
        if self.steps.step1 == 1:
            if form.cleaned_data['is_journey'] == False:
                self.form_list.pop('1')
            if form.cleaned_data['is_payed'] == False:
                self.form_list.pop('2')
        print self.form_list
        print self.steps
        return self.get_form_step_data(form)

    def done(self, form_list, **kwargs):
        
        event = form_list[0].save()
        if form_list[0].cleaned_data['is_journey'] == True:
            journey = form_list[1].save(commit = False)
            journey.event = event
            journey.save()
        if form_list[0].cleaned_data['is_payed'] == True:
            price_group = form_list[2].save(commit = False)
            price_group.event = event
            price_group.save()
        
        return redirect('event_added')

def add_journey_data_condition(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    return cleaned_data.get('is_journey', True)

def add_price_groups_condition(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    return cleaned_data.get('is_payed', True)

@login_required
@should_be_admin
def event_wizard(request):
    forms = [EventForm,
             JourneyDataForm,
             PriceGroupForm,
             EventMailForm,
             ]
    cond_dict = {'1': add_journey_data_condition,
                 '2': add_price_groups_condition,
                }
    return EventWizard.as_view(forms, condition_dict = cond_dict)(request)
'''
end of Wizard
'''

@login_required
@should_be_admin
def index(request):
    return render(request, 'events_admin_index.html')

@login_required
@should_be_admin
def show_all(request):
    events = Event.objects.all()
    return render(request, 'events_admin_show_all.html', { 'events' : events })

@login_required
@should_be_admin
def completed(request):
    return render(request, 'event_add_completed.html')
