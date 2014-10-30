from threading import local
from databases import databases

local_global = local()
local_global.subdomain = 'core_db'

class SubdomainMiddleware(object):
    
    def process_request(self, request):
	    def get_subdomain(request):
			try:
				host = request.META['HTTP_HOST'].split('.')
				if len(host) > 2:
					return host[0]
				else:
					return 'core_db' #FIXME 

			except: return 'core_db' #FIXME
	    local_global.subdomain =  get_subdomain(request)
