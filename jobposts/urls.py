from . import views
from django.urls import path


urlpatterns = [
    path('', views.JobList.as_view(), name='jobs'),
    # path('<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    path('job/<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    path('job/<int:job_post_id>/start_interview/', views.redirect_to_chatbot_index, name='start_interview'),
]
