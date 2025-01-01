from . import views
from django.urls import path


urlpatterns = [
    # path('', views.jobs_index, name='jobs'),
    path('', views.JobList.as_view(), name='jobs'),
]
