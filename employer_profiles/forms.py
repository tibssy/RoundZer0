from django import forms
from .models import Employer

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['company_name', 'phone']