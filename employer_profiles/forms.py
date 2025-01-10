from django import forms
from .models import Employer

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['company_name', 'phone', 'company_description']
        labels = {
            'company_name': 'Company Name',
            'phone': 'Phone Number',
            'company_description': 'Company Description',
        }
        widgets = {
            'company_description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'