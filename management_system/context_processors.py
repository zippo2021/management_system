from management_system.models import OrganisationSettings
from user_manager.permissions import perms_to_language
from middlewares import get_subdomain

def organisation_settings_processor(request):
	try:
		subdom = get_subdomain(request)
		settings = OrganisationSettings.objects.get(subdom = subdom)
	except:
		settings = 'Can not find settings for this subdom'
	return {'organisation_settings' : settings}

def permission_translation_processor(request):
	return {'perms_to_language' : perms_to_language}
