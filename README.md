Using Django==1.6.7

To install al the required packages try pip install -r requirements.txt 

Attention!!!
To use this version of project you'll need:


	1)in etc/hosts:
		change:
			127.0.0.1   localhost -----> 127.0.0.1 localhost.com
		
		add:
			127.0.0.1 sub1.localhost.com
			127.0.0.1 sub2.localhost.com
	
	2)create 2 additional DB (see settings.py)
		#! now you are ready to use subdom on your localhost

	3) run ./syncdb.sh	
	
	4) while syncdb you'll be able to create two additional superusers
	   for subdoms
	
	5)test subprojects on sub1.localhost.com
	  					  sub2.localhost.com
	#! attention don't use localhost.com with no subdom, or you may
	   add smth to core_db.

