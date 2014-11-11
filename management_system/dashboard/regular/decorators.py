from base_decorators import check_decorator
from dashboard import userdata
from functools import partial, wraps
from django.http import HttpResponse
from django.shortcuts import render, redirect
from dashboard import regular

#false functions

def not_regular(request, *args, **kwargs):
    if not(has_data(request)):
        return not_has_data(request)
    elif not(hasattr(request.user.UserData, 'RegularUser')):
        return not_has_regular_attr(request)
    else:
        return redirect('edit_regular')

not_has_regular_attr = lambda request, *args, **kwargs: render(request, 'decorator.html',
{'error' : "Here we have decorator working to prevent you from getting to this page, while you are NOT Regular"})

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
