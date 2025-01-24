"""
Custom signup form for user registration.

This form extends the default allauth signup form by adding a field to allow
the user to select their type (Candidate or Employer). Based on the selection,
the user is added to the appropriate group and their profile is created (either
Candidate or Employer).
"""

from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import Group
from candidate_profiles.models import Candidate
from employer_profiles.models import Employer


class CustomSignupForm(SignupForm):
    """
    Custom signup form that allows users to choose their role as either
    a 'Candidate' or an 'Employer'. Based on the selected role, the
    user is assigned to the appropriate group, and their corresponding
    profile (Candidate or Employer) is created.
    """

    USER_TYPE_CHOICES = (
        ('candidate', 'Candidate'),
        ('employer', 'Employer')
    )
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        label='I am a',
        widget=forms.Select
    )

    def save(self, request):
        """
        Save the user form and create a user profile based on the selected
        user type. The user is added to the respective group ('Candidate' or
        'Employer'), and their profile is created accordingly.

        Args:
            request: The HTTP request object.

        Returns:
            user: The user instance after saving and associating with the group
                  and profile.
        """

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
