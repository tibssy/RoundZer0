from django import forms
from .models import JobPost


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['title', 'company_name', 'location', 'employment_type', 'description', 'responsibilities', 'requirements', 'benefits', 'application_deadline']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g., Senior Software Engineer'}),
            'company_name': forms.TextInput(attrs={'placeholder': 'e.g., Tech Innovations Inc.'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g., Dublin, IE'}),
            'employment_type': forms.Select(attrs={'placeholder': 'Select Employment Type'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe the job role and company'}),
            'responsibilities': forms.Textarea(attrs={'placeholder': 'List the main responsibilities'}),
            'requirements': forms.Textarea(attrs={'placeholder': 'Specify the required skills and qualifications'}),
            'benefits': forms.Textarea(attrs={'placeholder': 'Outline the employee benefits'}),
            'application_deadline': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
        }