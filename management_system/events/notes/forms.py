
from django.forms import ModelForm
from events.notes.models import Note

class NoteForm(ModelForm):
    class Meta:
        model = Note
        exclude = ['author',
                   'receiver',
                   ]
