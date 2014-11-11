from django.shortcuts import render, redirect
from functools import partial, wraps
from base_decorators import check_decorator
from dashboard.observer.decorators import is_observer
from dashboard.mentor.decorators import is_mentor
from dashboard.event_worker.decorators import is_event_worker
from dashboard.teacher.decorators import is_teacher
from dashboard.regular.decorators import is_regular


#false functions

not_has_data = lambda request, *args, **kwargs: redirect('edit_userdata')
not_defined = lambda request, *args, **kwargs: not_regular(request)\
                if has_data(request) else not_has_data(request)


#condition functions

has_data = lambda request, *args, **kwargs:\
            request.user.UserData.modified\
            if hasattr(request.user, 'UserData') else False
is_defined = lambda request, *args, **kwargs:\
                (is_observer(request, *args, **kwargs) or
                 is_mentor(request, *args, **kwargs) or
                 is_event_worker(request, *args, **kwargs) or
                 is_teacher(request, *args, **kwargs) or
                 is_regular(request, *args, **kwargs))

#decorators

should_have_data = partial(check_decorator,
                           condition_func = has_data,
						   false_func = not_has_data)
should_be_defined = partial(check_decorator,
                           condition_func = is_defined,
						   false_func = not_defined)

