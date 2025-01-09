from django import forms
from .models import Candidate


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    class Meta:
        model = Candidate
        fields = ['phone', 'executive_summary', 'key_skills']
        labels = {
            'phone': 'Phone Number',
            'executive_summary': 'Executive Summary / About Me',
            'key_skills': 'Key Skills',
        }
        widgets = {
            'executive_summary': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'