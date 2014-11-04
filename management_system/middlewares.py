from threading import local
from databases import databases, subdoms
from django.core.exceptions import PermissionDenied

local_global = local()
local_global.subdomain = 'core_db'

class SubdomainMiddleware(object):
    
    def process_request(self, request):
	    def get_subdomain(request):
			try:
				subdomain = request.META['HTTP_HOST'].split('.')[0]
				if subdomain in subdoms:
					return subdomain
				else:
					raise PermissionDenied 
			
			except: raise PermissionDenied #FIXME
	    local_global.subdomain =  get_subdomain(request)
