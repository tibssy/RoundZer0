from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import Group
from candidate_profiles.models import Candidate
from employer_profiles.models import Employer

class CustomSignupForm(SignupForm):
    USER_TYPE_CHOICES = (
        ('candidate', 'Candidate'),
        ('employer', 'Employer')
    )
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        label="I am a",
        widget=forms.Select
    )

    def save(self, request):
        user = super().save(request)
        user_type = self.cleaned_data['user_type']
        group = None
        if user_type == 'employer':
            group = Group.objects.get(name='Employer')
            Employer.objects.create(user=user)
        elif user_type == 'candidate':
            group = Group.objects.get(name='Candidate')
            Candidate.objects.create(user=user)

        if group:
            user.groups.add(group)
            user.save()

        return user