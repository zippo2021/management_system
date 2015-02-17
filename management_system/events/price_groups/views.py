from django.shortcuts import render
from events.price_groups.forms import PriceGroupForm
from events.price_groups.models import PriceGroup
from events.events_admin.models import Event
# Create your views here.

def add(request,eid):
    if request.method == "POST":
        form = PriceGroupForm(request.POST)
        if form.is_valid():
            event = Event.objects.get(id = eid)
            pg = PriceGroup(event = event, price = form.cleaned_data['price'])
            pg.save()
            return render(request,"price_group_completed.html",{'eid':eid})
    else:
        form = PriceGroupForm()
        return render(request,"price_group_form.html",{'form':form})

def show(request,eid):
    event = Event.objects.get(id = eid)
    p_groups = event.PriceGroup.all()
    return render(request,'price_group_show.html',{'p_groups':p_groups,'eid':eid})
    
