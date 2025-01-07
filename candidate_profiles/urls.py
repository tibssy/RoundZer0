from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.candidate_profile, name='candidate_profile'),
    path('delete_profile/', views.delete_profile_and_account, name='delete_profile_and_account'),
]