from management_system.models import OrganisationSettings
from user_manager.permissions import perms_to_language
from dashboard.userdata.documents import docs_to_language
from dashboard.common_profile.source_functions import perms_to_list
from events.events_admin.models import Event
from middlewares import get_subdomain
from django.db.models import Q

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
    perms = perms_to_list(request.user.UserData.get_permissions())
    return {'user_permissions' : perms}

def events_processor(request):
    events = Event.objects.all()
    user = request.user.UserData
    if not(user.Admin.is_active):
        events = events.filter(Q(event_workers = user.EventWorker)
                                            | Q(teachers = user.Teacher)
                                            | Q(mentors = user.Mentor)
                                            | Q(observers = user.Observer))
    active_events = events.filter(is_active = True)
    archive_events = events.filter(is_active = False)
    return {'ative_events' : active_events, ' archive_events' : archive_events}
