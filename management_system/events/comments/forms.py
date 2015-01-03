from django.forms import ModelForm
from events.comments.models import PersonalComment

class PersonalCommentForm(ModelForm):
    class Meta:
        model = PersonalComment
        exclude = ['event']
