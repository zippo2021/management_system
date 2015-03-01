from management_system.models import OrganisationSettings
from user_manager.permissions import perms_to_language
from dashboard.userdata.documents import docs_to_language
from dashboard.common_profile.source_functions import perms_to_list
from events.events_admin.models import Event
from middlewares import get_subdomain
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date


def organisation_settings_processor(request):
	try:
		subdom = get_subdomain(request)
		settings = OrganisationSettings.objects.get(subdom = subdom)
	except:
		settings = 'Can not find settings for this subdom'
	return {'organisation_settings' : settings}

def permission_translation_processor(request):
	return {'perms_to_language' : perms_to_language}

def documents_translation_processor(request):
    return {'docs_to_language' : docs_to_language}


def user_permissions_processor(request):
    if request.user.is_authenticated():      
        perms = perms_to_list(request.user.UserData.get_permissions())
        return {'user_permissions' : perms}
    else:
        return {}

def events_processor(request):
    if request.user.is_authenticated():    
        events = Event.objects.all()
        user = request.user.UserData
        if not(user.Admin.is_active):   
            events = events.filter(Q(event_workers = user.EventWorker)
                                            | Q(teachers = user.Teacher)
                                            | Q(mentors = user.Mentor)
                                            | Q(observers = user.Observer))
        active_events = events.filter(is_active = True)
        archive_events = events.filter(is_active = False)   
        archive_events_by_year = {}
        start_year = 2014
        end_year = date.today().year
        for each in xrange(start_year, end_year+1):
            archive_events_by_year.update(
                    { each : archive_events.filter(closed__year = each)}
            )
        print archive_events_by_year
        return {'active_events' : active_events,
                'archive_events_by_year' : archive_events_by_year}
    else:
        return {}
