from django.shortcuts import render, redirect
from functools import partial, wraps
from django.http import HttpResponse
from base_decorators import check_decorator


#false functions

not_event_worker = lambda request, *args, **kwargs: render(request, 'decorator.html',
{'error' : "Here we have decorator working to prevent you from getting to this page, while you are NOT EventWorker"})

#codition functions 

is_event_worker = lambda request, *args, **kwargs:\
                hasattr(request.user.UserData, 'Event_Worker')\
				if has_data(request) else False

#decorators

should_be_event_worker =  partial(check_decorator,
                                  condition_func = is_event_worker,
								  false_func = not_event_worker)

