from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.candidate_profile, name='candidate_profile'),
    path('profile/edit/', views.edit_candidate_profile, name='edit_candidate_profile'),
    path('profile/history/', views.candidate_history, name='candidate_history'),
    path('delete_profile/', views.delete_candidate_profile, name='delete_candidate_profile'),
    path('interview/delete/<int:interview_id>/', views.delete_interview, name='delete_interview'),
]