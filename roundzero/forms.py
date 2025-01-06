from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import Group

class CustomSignupForm(SignupForm):
    USER_TYPE_CHOICES = (
        ('employer', 'Employer'),
        ('candidate', 'Candidate'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, label="I am a", widget=forms.RadioSelect)

    def save(self, request):
        user = super().save(request)
        user_type = self.cleaned_data['user_type']
        group = None
        if user_type == 'employer':
            group = Group.objects.get(name='Employer')
        elif user_type == 'candidate':
            group = Group.objects.get(name='Candidate')

        if group: #check if group exists
            user.groups.add(group)
            user.save()

        return user