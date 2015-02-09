from databases import databases


class SubdomainRouter(object):
    def db_for_read(self, model, **hints):
        from middlewares import local_global
        from databases import databases
        if not(local_global.subdomain == None):
            return databases[local_global.subdomain]
        else:
            return None

    def db_for_write(self, model, **hints):
		from middlewares import local_global
		from databases import databases
		if not(local_global.subdomain == None):
			return databases[local_global.subdomain]
		else:
			return None

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_syncdb(self, db, model):
		return True

