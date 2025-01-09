from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.candidate_profile, name='candidate_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/history/', views.candidate_history, name='candidate_history'),
    path('delete_profile/', views.delete_profile_and_account, name='delete_profile_and_account'),
]