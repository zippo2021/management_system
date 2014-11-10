from management_system.models import OrganisationSettings
from middlewares import get_subdomain

def organisation_settings_processor(request):
	try:
		subdom = get_subdomain(request)
		settings = OrganisationSettings.objects.get(subdom = subdom)
	except:
		settings = 'Can not find settings for this subdom'
	return {'organisation_settings': settings}
