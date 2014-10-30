from threading import local
from databases import databases

local_global = local()
local_global.subdomain = None

class SubdomainMiddleware(object):
    
    def process_request(self, request):
	    def get_subdomain(request):
	    try: return request.META['HTTP_HOST'].split('.')[0]
	    except: return None
	
	    local_global.subdomain =  get_subdomain(request)
