from django.shortcuts import render, redirect
from functools import partial, wraps
from django.http import HttpResponse
from base_decorators import check_decorator



#false functions

not_teacher = lambda request, *args, **kwargs: render(request, 'decorator.html',
{'error' : "Here we have decorator working to prevent you from getting to this page, while you are NOT Teacher"})

#condition functions

is_teacher = lambda request, *args, **kwargs:\
                hasattr(request.user.UserData, 'Teacher')\
				if has_data(request) else False

#decorators

should_be_teacher = partial(check_decorator,
                            condition_func = is_teacher,
							false_func = not_teacher)

