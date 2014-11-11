from django.shortcuts import render, redirect
from functools import partial, wraps
from django.http import HttpResponse
from base_decorators import check_decorator



#false functions

not_mentor = lambda request, *args, **kwargs: render(request, 'decorator.html', {'error' : "Here we have decorator working to prevent you from getting to this page, while you are NOT Mentor"})


#condition functions

is_mentor = lambda request, *args, **kwargs:\
                hasattr(request.user.UserData, 'Mentor')\
				if has_data(request) else False

#decorators

should_be_mentor =  partial(check_decorator,
                            condition_func = is_mentor,
							false_func = not_mentor)

