from . import views
from django.urls import path


urlpatterns = [
    path('', views.JobList.as_view(), name='jobs'),
    path('<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
]
