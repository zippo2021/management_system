from django.shortcuts import render, redirect
from events.price_groups.forms import PriceGroupForm
from events.price_groups.models import PriceGroup
from events.events_admin.models import Event
# Create your views here.

def add(request, event_id):
    if request.method == "POST":
        form = PriceGroupForm(request.POST)
        if form.is_valid():
            event = Event.objects.get(id = event_id)
            pg = PriceGroup(event = event, price = form.cleaned_data['price'])
            pg.save()
            return redirect('completed')
    else:
        form = PriceGroupForm()
        return render(request,"price_group_form.html",{'form':form})

def show(request, event_id):
    event = Event.objects.get(id = event_id)
    p_groups = event.PriceGroup.all()
    return render(request,'price_group_show.html',{'p_groups':p_groups,
                        'eid':event_id})
    
