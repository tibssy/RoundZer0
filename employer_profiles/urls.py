from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.employer_profile, name='employer_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('delete_profile/', views.delete_profile_and_account, name='delete_profile_and_account'),
]