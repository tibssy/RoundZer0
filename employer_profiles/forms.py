"""
Django form for editing an employer's profile.

This module contains the form used to edit the employer's profile,
including fields like company name, phone number, and company description.
"""

from django import forms
from .models import Employer


class EditProfileForm(forms.ModelForm):
    """
    Form for editing the employer's profile.

    This form allows users to edit their company name, phone number,
    and company description. It also applies custom styling to the form fields.
    """

    class Meta:
        """Configuration for the EditProfileForm."""
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
        """
        Initializes the form and applies custom CSS class to fields.

        This method sets the 'form-control' CSS class for each field in
        the form.
        """

        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
