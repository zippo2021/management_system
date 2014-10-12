from threading import local
from django.contrib.sessions.models import Session

local_global = local()

class KeywordMiddleware(object):
    def process_request(self, request):
	local_global.keyword = get_database_name(request)

    def get_database_name(request):
	session_key = request.session.session_key
    
	session = Session.objects.get(session_key = session_key)
	return session.get_decoded().get('keyword')
