#-*- coding: utf-8 *-*
from threading import local
from databases import databases, subdoms
from django.core.exceptions import PermissionDenied

local_global = local()
local_global.subdomain = None

translate_subdoms = {'цпм':'cpm','sub1':'sub1','sub2':'sub2'}

def get_subdomain(request):
	try:
		subdomain = request.META['HTTP_HOST'].split('.')[0]
		if subdomain in subdoms:
			return translate_subdoms[subdomain]
		else:
			raise PermissionDenied 

	except: raise PermissionDenied #FIXME

class SubdomainMiddleware(object):
	def process_request(self, request):
	    local_global.subdomain =  get_subdomain(request)
