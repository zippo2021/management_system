from databases import databases

class KeywordRouter(object):
    def db_for_read(self, model, databases):
	from middleware import local_global
	return databases['local_global']

    def db_for_write(self, model, databases):
	from middleware import local_global
	return databases['local_global']
    
    def allow_relation(self, obj1, obj2, databases):
	return None

    def allow_syncdb(self, db, model):
	return True

class CoreRouter(object):
    def db_for_read(self, model, **hints):
	if model._meta.app_label == 'web_core':
	    return 'core_db'
	if model._meta.app_label == 'sessions':
	    return 'core_db'
	return None

    def db_for_write(self, model, **hints):
	if model._meta.app_label == 'web_core':
	    return 'core_db'
	if model._meta.app_label == 'sessions':
	    return 'core_db'
	return None

    def allow_relation(self, obj1, obj2, **hints):
	if obj1._meta.app_label == 'web_core' or\
	   obj2._meta.app_label == 'web_core':
	    return True
	
	if obj1._meta.app_label == 'sessions' or\
	   obj2._meta.app_label == 'sessions':
	    return True

	return None

    def allow_syncdb(self, db, model):
	return True
