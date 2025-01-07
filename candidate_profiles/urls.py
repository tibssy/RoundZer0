from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.candidate_profile, name='candidate_profile'),
]