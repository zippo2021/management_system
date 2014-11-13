from functools import partial, wraps
from django.http import HttpResponse
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
define decorators
'''

	#false functions

not_defined = lambda request, *args, **kwargs: not_regular(request)\
				if has_data(request) else not_has_data(request)

	#condition functions

is_defined = lambda request, *args, **kwargs:\
				(is_observer(request, *args, **kwargs) or
				is_mentor(request, *args, **kwargs) or 
				is_event_worker(request, *args, **kwargs) or
				is_teacher(request, *args, **kwargs) or
				is_regular(request, *args, **kwargs))

	#decorators

should_be_defined = partial(check_decorator,
							condition_func = is_defined,
							false_func = not_defined)

'''
userdata decorators
'''

	#false functions

not_has_data = lambda request, *args, **kwargs: redirect('edit_userdata')

	#condition functions

has_data = lambda request, *args, **kwargs:\
			request.user.UserData.modified\
			if hasattr(request.user, 'UserData') else False

	#decorators

should_have_data = partial(check_decorator,
						   condition_func = has_data,
						   false_func = not_has_data)
'''
regular decorators
'''

	#false functons

not_has_regular_attr = lambda request, *args, **kwargs: render(request, 'decorator.html',
{'error' : "Here we have decorator working to prevent you from getting to this page, while you are NOT Regular"})


def not_regular(request, *args, **kwargs):
	if not(has_data(request)): 
		return not_has_data(request)
	elif not(hasattr(request.user.UserData, 'RegularUser')):
		return not_has_regular_attr(request)
	else:
		return redirect('edit_regular')

	#condition functions

has_regular_attr = lambda request, *args, **kwargs:\
				hasattr(request.user.UserData, 'RegularUser')

is_regular = lambda request, *args, **kwargs:\
				request.user.UserData.RegularUser.modified\
				if hasattr(request.user.UserData, 'RegularUser')\
				and  has_data(request) else False

	#decorators

should_be_regular = partial(check_decorator,
							condition_func = is_regular,
							false_func = not_regular)

should_have_regular_attr = partial(check_decorator,
						   condition_func = has_regular_attr,
						   false_func = not_has_regular_attr)

'''
teacher decorators
'''

	#false functions

not_teacher = lambda request, *args, **kwargs: render(request, 'decorator.html',
{'error' : "Here we have decorator working to prevent you from getting to this page, while you are NOT Teacher"})

	#condition functions

is_teacher = lambda request, *args, **kwargs:\
				request.user.UserData.is_teacher\
				if has_data(request) else False

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
				request.user.UserData.is_event_worker\
				if has_data(request) else False

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
				request.user.UserData.is_mentor\
				if has_data(request) else False

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
				request.user.UserData.is_observer\
				if has_data(request) else False

	#decorators

should_be_observer =  partial(check_decorator,
                              condition_func = is_observer,
							  false_func = not_observer)

