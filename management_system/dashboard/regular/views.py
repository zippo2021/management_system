from django.shortcuts import render, redirect
from dashboard.regular.models import RegularUser
from dashboard.regular.forms import RegularUserForm, RegularUserFormStep1, RegularUserFormStep2, RegularUserFormStep3
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from decorators import  should_be_regular, should_be_defined,should_be_staff
from django.core.exceptions import ObjectDoesNotExist
from decorators import should_be_regular_possibly_unfilled, should_be_regular
from django.http import HttpResponse
from django.contrib.formtools.wizard.views import SessionWizardView



'''
Wizard:
it includes Wizard class with .done() and special wrapper function,
which imitates view function (also loads instances and forms)
so you can access wizard as a simple view, named regular_user_wizard
'''
class RegularUserWizard(SessionWizardView):
    template_name = 'regular_edit_wizard.html'
    def done(self, form_list, **kwargs):
        '''
        it's a little bit funny, but there is no need to save first
        steps, because they're using one instance (with third step),
        so they update it
        '''
        #regular = form_list[0].save(commit = False)
        #regular = form_list[1].save(commit = False)
        '''
        end of funny moment. The only line that's needed is below.
        '''
        regular = form_list[2].save(commit = False)
        regular.modified = True
        regular.save()
        return redirect('regular_edited')

@login_required
@should_be_regular_possibly_unfilled
def regular_user_wizard(request):
    instance = request.user.UserData.RegularUser
    inst_dict = { '0' : instance,
                  '1' : instance,
                  '2' : instance,
                }
    forms = [RegularUserFormStep1,
             RegularUserFormStep2,
             RegularUserFormStep3
            ]
    return RegularUserWizard.as_view(forms, instance_dict = inst_dict)(request)
'''
end of Wizard
'''

@login_required
@should_be_regular_possibly_unfilled
def edit(request):
    if request.method == 'POST':
        form = RegularUserForm(request.POST,
			   instance = request.user.UserData.RegularUser)
        if form.is_valid():
            regular = form.save(commit = False)
            regular.modified = True
            regular.save()
            return redirect('regular_edited')
    else:
		form = RegularUserForm(instance = request.user.UserData.RegularUser)
	
    return render(request, 'regular_edit.html', {'form' : form})

@login_required
@should_be_regular
def completed(request):
        request.session['UserDataModal'] = 'off'
	return render(request, 'regular_completed.html')




