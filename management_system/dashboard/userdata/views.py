# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from dashboard.userdata.forms import UserDataForm, PassportForm, ZagranForm, BirthCertForm, OtherDocForm, DocumentTypeForm
from dashboard.userdata.models import UserData
from decorators import should_be_defined
from django.http import HttpResponse
from django.contrib.formtools.wizard.views import SessionWizardView
from dashboard.userdata.documents import docs_to_classes

'''
Wizard:
it includes Wizard class with .done() and special wrapper function,
which imitates view function (also loads instances and forms)
so you can access wizard as a simple view, named regular_user_wizard
'''
class DocumentWizard(SessionWizardView):
    template_name = 'userdata_document_wizard.html'
    def done(self, form_list, **kwargs):
        if form_list[0].cleaned_data['type'] == 'P':
            if hasattr(self.request.user.UserData, 'Passport'):
               self.request.user.UserData.Passport.delete() 
            passport = form_list[1].save(commit = False)
            passport.user = self.request.user.UserData
            passport.save()
        elif form_list[0].cleaned_data['type'] == 'Z':
            if hasattr(self.request.user.UserData, 'Zagran'):
               self.request.user.UserData.Zagran.delete() 
            zagran = form_list[1].save(commit = False)
            zagran.user = self.request.user.UserData
            zagran.save()
        elif form_list[0].cleaned_data['type'] == 'B':
            if hasattr(self.request.user.UserData, 'BirthCert'):
               self.request.user.UserData.BirthCert.delete() 
            birth_cert = form_list[1].save(commit = False)
            birth_cert.user = self.request.user.UserData
            birth_cert.save()
        elif form_list[0].cleaned_data['type'] == 'O':
            if hasattr(self.request.user.UserData, 'OtherDoc'):
               self.request.user.UserData.BirthCert.delete() 
            other = form_list[1].save(commit = False)
            other.user = self.request.user.UserData
            other.save()
        return redirect('completed')

def add_passport_condition(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    return cleaned_data.get('type') == 'P'
    
def add_zagran_condition(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    return cleaned_data.get('type') == 'Z'
    
def add_birth_cert_condition(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    return cleaned_data.get('type') == 'B'
    
def add_other_condition(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    return cleaned_data.get('type') == 'O'

@login_required
def document_wizard(request):
    forms = [DocumentTypeForm,
             PassportForm,
             ZagranForm,
             BirthCertForm,
             OtherDocForm
             ]
    cond_dict = {'1' : add_passport_condition,
                 '2' : add_zagran_condition,
                 '3' : add_birth_cert_condition,
                 '4' : add_other_condition
                 }
    return DocumentWizard.as_view(forms, condition_dict = cond_dict)(request)
'''
end of Wizard
'''

@login_required
def edit(request):
    if request.method == 'POST':
		#userdata always exists if we passed should_have_data
		form = UserDataForm(request.POST, instance = request.user.UserData)
		#validate form and redirect
		if form.is_valid():
			user_data = form.save(commit = False)
			user_data.modified = True
			user_data.save()
			return redirect('completed')
    else:		
        form = UserDataForm(instance = request.user.UserData)

	return render(request, 'userdata_form.html', {'form' : form})
