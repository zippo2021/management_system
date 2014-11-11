from dashboard.userdata.decorators import has_data
from django.shortcuts import render, redirect
from functools import partial, wraps
from django.http import HttpResponse
from base_decorators import check_decorator


#false function

not_observer = lambda request, *args, **kwargs: render(request, 'decorator.html',
{'error' : "Here we have decorator working to prevent you from getting to this page, while you are NOT Observer"})


#condition functions

is_observer = lambda request, *args, **kwargs:\
                hasattr(request.user.UserData, 'Observer')\
				if has_data(request) else False

#decorators

should_be_observer =  partial(check_decorator,
                              condition_func = is_observer,
							  false_func = not_observer)

