from django import forms
from .models import Candidate


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    email = forms.EmailField(label='Email')

    class Meta:
        model = Candidate
        fields = ['phone', 'resume']
        labels = {
            'phone': 'Phone Number',
            'resume': 'Upload New Resume',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'