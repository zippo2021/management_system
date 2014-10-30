from databases import databases


class KeywordRouter(object):
    def db_for_read(self, model, **hints):
	from middlewares import local_global
	from databases import databases
	print model._meta.app_label, ' KeywordRouter'
	return databases[local_global.keyword]

    def db_for_write(self, model, **hints):
	from middlewares import local_global
	from databases import databases
	return databases[local_global.keyword]
    
    def allow_relation(self, obj1, obj2, **hints):
	return None

    def allow_syncdb(self, db, model):
	return True

class CoreRouter(object):
    def db_for_read(self, model, **hints):
	if model._meta.app_label == 'web_core':
	    return databases['core_db']
	    print 'webcore'
	if model._meta.app_label == 'sessions':
	    print 'session'
	    return databases['core_db']
	return None

    def db_for_write(self, model, **hints):
	if model._meta.app_label == 'web_core':
	    return databases['core_db']
	if model._meta.app_label == 'sessions':
	    return databases['core_db']
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
