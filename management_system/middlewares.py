from threading import local
from django.contrib.sessions.models import Session
from databases import databases

local_global = local()

class KeywordMiddleware(object):
    
    def process_request(self, request):
	def get_keyword(request):
	    try: return request.session['keyword']
	    except: return 'core_db'
	
	local_global.keyword =  get_keyword(request)

