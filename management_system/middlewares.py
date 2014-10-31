from threading import local
from databases import databases

local_global = local()
local_global.subdomain = 'core_db'

class SubdomainMiddleware(object):
    
    def process_request(self, request):
	    def get_subdomain(request):
			try:
				subdomain = request.META['HTTP_HOST'].split('.')[0]
				if subdomain in databases.keys():
					return subdomain
				else:
					return 'else!!!' #FIXME 

			except: return 'except!!!' #FIXME
	    local_global.subdomain =  get_subdomain(request)
