from functools import partial, wraps
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from dashboard import userdata
from dashboard import regular


def check_decorator(view=None,
              condition_func = lambda request, *args, **kwargs: True,
	          false_func = lambda request, *args, **kwargs: HttpResponse()):
    '''
   Checks by :function:condition_func, if true go to :function: view,
   else go to :function:false_func
   :param condition_func: Should return Boolean value
   :type condition_func: function
   :param false_func: Should return object of :class:`http.HttpResponse'
   :return: :class:`http.HttpResponse`
    '''
    def decorator(view):
		@wraps(view)
		def wrapper(request, *args, **kwargs):
			if not condition_func(request, *args, **kwargs):
				return false_func(request, *args, **kwargs)
			return view(request, *args, **kwargs)
		return wrapper
    return decorator(view) if view else decorator

'''
document decorators
'''

    #false functions

not_has_document = lambda request, *args, **kwags: redirect('edit document')

    #condition functions

has_document = lambda request, *args, **kwargs: not_has_filled_data(request)\
               if not has_filled_data(request)\
               else request.user.UserData.Zagran\
                or request.user.UserData.BirthCert\
                or request.user.UserData.Passport\
                or request.user.UserData.OtherDoc
                
    #decorators

should_be_defined = partial(check_decorator,
							condition_func = has_document,
							false_func = not_has_document)


'''
define decorators
'''

	#false functions

not_defined = lambda request, *args, **kwargs: not_regular(request)\
				if has_filled_data(request) else not_has_filled_data(request)

	#condition functions

is_defined = lambda request, *args, **kwargs:\
				(is_observer(request, *args, **kwargs) or
				is_mentor(request, *args, **kwargs) or 
				is_event_worker(request, *args, **kwargs) or
				is_teacher(request, *args, **kwargs) or
				is_regular(request, *args, **kwargs) or
				is_admin(request, *args, **kwargs))

	#decorators

should_be_defined = partial(check_decorator,
							condition_func = is_defined,
							false_func = not_defined)

'''
userdata decorators
'''

	#false functions

not_has_filled_data = lambda request, *args, **kwargs: redirect('userdata_edit')

	#condition functions

has_filled_data = lambda request, *args, **kwargs:\
			request.user.UserData.modified

	#decorators

should_have_filled_data = partial(check_decorator,
						   condition_func = has_filled_data,
						   false_func = not_has_filled_data)
'''
regular decorators
'''

	#false functons

not_is_regular_possibly_unfilled = lambda request, *args, **kwargs: render(request, 'decorator.html',
{'error' : "Here we have decorator working to prevent you from getting to this page, while you are NOT Regular"})


def not_regular(request, *args, **kwargs):
	if not(has_filled_data(request)): 
            return not_has_filled_data(request)
	elif not(is_regular_possibly_unfilled(request)):
            return not_is_regular_possibly_unfilled(request)
	else:
            request.session['UserDataModal'] = 'on'
            return (request.path)


	#condition functions

is_regular_possibly_unfilled = lambda request, *args, **kwargs:\
								request.user.UserData.RegularUser.is_active
				
is_regular = lambda request, *args, **kwargs:\
				request.user.UserData.RegularUser.modified\
				if is_regular_possibly_unfilled(request)\
				and  has_filled_data(request) else False


	#decorators

should_be_regular = partial(check_decorator,
							condition_func = is_regular,
							false_func = not_regular)

should_be_regular_possibly_unfilled = partial(check_decorator,
						  	condition_func = is_regular_possibly_unfilled,
						   	false_func = not_is_regular_possibly_unfilled)

'''
teacher decorators
'''

	#false functions

not_teacher = lambda request, *args, **kwargs: render(request, 'decorator.html',
{'error' : "Here we have decorator working to prevent you from getting to this page, while you are NOT Teacher"})

	#condition functions

is_teacher = lambda request, *args, **kwargs:\
				request.user.UserData.Teacher.is_active\
				if has_filled_data(request) else False

	#decorators

should_be_teacher = partial(check_decorator,
							condition_func = is_teacher,
							false_func = not_teacher)

'''
event_worker decorators
'''

	#false functions

not_event_worker = lambda request, *args, **kwargs: render(request, 'decorator.html',
{'error' : "Here we have decorator working to prevent you from getting to this page, while you are NOT EventWorker"})

	#condition fucntions

is_event_worker = lambda request, *args, **kwargs:\
				request.user.UserData.EventWorker.is_active\
				if has_filled_data(request) else False

	#decorators

should_be_event_worker =  partial(check_decorator,
                            	  condition_func = is_event_worker,
								  false_func = not_event_worker)

'''
mentor decorators
'''

	#false functions

not_mentor = lambda request, *args, **kwargs: render(request, 'decorator.html', {'error' : "Here we have decorator working to prevent you from getting to this page, while you are NOT Mentor"})

	#condition functions

is_mentor = lambda request, *args, **kwargs:\
				request.user.UserData.Mentor.is_active\
				if has_filled_data(request) else False

	#decorators

should_be_mentor =  partial(check_decorator,
                            condition_func = is_mentor,
							false_func = not_mentor)

'''
observer decorators
'''

	#false functions

not_observer = lambda request, *args, **kwargs: render(request, 'decorator.html', 
{'error' : "Here we have decorator working to prevent you from getting to this page, while you are NOT Observer"})

	#condition functions

is_observer = lambda request, *args, **kwargs:\
				request.user.UserData.Observer.is_active\
				if has_filled_data(request) else False

	#decorators

should_be_observer =  partial(check_decorator,
                              condition_func = is_observer,
							  false_func = not_observer)

'''
Admin decorator
'''
    #false functions
not_admin = lambda request, *args, **kwargs: render(request, 'decorator.html', 
{'error' : "Here we have decorator working to prevent you from getting to this page, while you are NOT Admin"})



    #condition functions

is_admin = lambda request, *args, **kwargs:\
             request.user.UserData.Admin.is_active\
             if has_filled_data(request) else False
	
    #decorators

should_be_admin =  partial(check_decorator,
                           condition_func = is_admin,
						   false_func = not_admin)

'''
Staff decorator
'''
    #condition functions

is_staff = lambda request, *args, **kwargs: True\
				if is_teacher(request) or\
                is_mentor(request) or\
                is_observer(request) or\
                is_event_worker(request) or\
                is_admin(request)\
                else False 
    #false functions

not_staff = lambda request, *args, **kwargs: render(request, 'decorator.html', {'error' : "Here we have decorator working to prevent you from getting to this page, while you are NOT staff"})

    #decorators

should_be_staff = partial(check_decorator,
                              condition_func = is_staff,
							  false_func = not_staff)
