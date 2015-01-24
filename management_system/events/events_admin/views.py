from django.shortcuts import render
from events.events_admin.models import Event
from decorators import staff_member_required

@login_required
@staff_member_required
def add(request):
    if request.method == 'POST':
        form = CreateEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_created')

    else:
        form = CreateEventForm()

    return render(request, 'event_admin_add.html', {'form' : form})

@staff_member_required
def completed(request):
    return render(request, 'event_admin_completed.html')
