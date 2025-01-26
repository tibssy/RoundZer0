"""
Forms for managing candidate profiles.

This module contains the form used for editing candidate profiles,
including fields for personal and professional details.
"""

from django import forms
from .models import Candidate


class EditProfileForm(forms.ModelForm):
    """
    A form for editing candidate profiles.

    Allows editing of phone number, executive summary, and key skills.
    It also pre-populates the first and last name fields based on the
    associated user instance.

    Attributes:
        first_name (CharField): The first name of the candidate.
        last_name (CharField): The last name of the candidate.

    Meta:
        model: Candidate
            The model associated with this form.
        fields: list
            The fields to include in the form.
        labels: dict
            Custom labels for the fields.
        widgets: dict
            Custom widgets for specific fields.

    Methods:
        __init__(self, *args, **kwargs):
            Initializes the form and sets initial values for
            first and last name based on the candidate's user instance.
    """

    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    class Meta:
        """Configuration for the EditProfileForm."""
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
        """
        Initialize the form with custom styling and initial values.

        Args:
            *args: Variable-length argument list.
            **kwargs: Arbitrary keyword arguments.
        """

        super().__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
