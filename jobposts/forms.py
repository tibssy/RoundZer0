from django import forms
from .models import JobPost


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['title', 'company_name', 'location', 'employment_type', 'description', 'responsibilities', 'requirements', 'benefits', 'application_deadline']
        widgets = {
            'application_deadline': forms.DateInput(attrs={'type': 'date'}),
        }