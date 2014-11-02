from functools import partial
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

has_data = lambda user: hasattr(user, 'UserData')
is_teacher = lambda request, *args, **kwargs: 
				hasattr(request.user.UserData.Teacher)
				if has_data(request.user) else False
is_event_worker = lambda request, *args, **kwargs:
				hasattr(request.user.UserData.Event_Worker)
				if has_data(request.user) else False
is_mentor = lambda request, *args, **kwargs:
				hasattr(request.user.UserData.Mentor)
				if has_data(request.user) else False
is_observer = lambda request, *args, **kwargs:
				hasattr(request.user.UserData.Observer)
				if has_data(request.user) else False

should_be_teacher = partial(check_decorator,
							conditiom_func = is_teacher,
							false_func = 

