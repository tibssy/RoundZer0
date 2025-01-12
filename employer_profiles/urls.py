from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.employer_profile, name='employer_profile'),
    path('profile/edit/', views.edit_employer_profile, name='edit_employer_profile'),
    path('delete_profile/', views.delete_employer_profile, name='delete_employer_profile'),
    path('my_jobs/', views.my_jobs, name='employer_jobs'),
]