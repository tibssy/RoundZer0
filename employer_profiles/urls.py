from django.urls import path
from . import views
from candidate_profiles import views as candidate_views
from jobposts import views as jobpost_views


urlpatterns = [
    path('profile/', views.employer_profile, name='employer_profile'),
    path('profile/edit/', views.edit_employer_profile, name='edit_employer_profile'),
    path('delete_profile/', views.delete_employer_profile, name='delete_employer_profile'),
    path('my_jobs/', views.my_jobs, name='employer_jobs'),
    path('my_jobs/create/', views.create_job, name='create_job'),
    path('my_jobs/view/<int:pk>/', jobpost_views.JobDetailView.as_view(), name='view_my_job'),
    path('my_jobs/edit/<int:job_id>/', views.edit_my_jobs, name='edit_my_jobs'),
    path('my_jobs/delete/<int:job_id>/', views.delete_my_job, name='delete_my_job'),
    path('my_jobs/applications/<int:job_id>/', views.job_applications, name='job_applications'),
    path('candidate/<int:candidate_id>/', candidate_views.candidate_profile_view, name='candidate_profile_view'),
]