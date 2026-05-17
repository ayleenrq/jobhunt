from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.JobListView.as_view(), name='job-list'),
    path('jobs/<int:pk>/', views.JobDetailView.as_view(), name='job-detail'),
    path('saved/', views.SavedJobListView.as_view(), name='saved-job-list'),
    path('saved/<int:pk>/', views.SavedJobDetailView.as_view(), name='saved-job-detail'),
    path('alerts/', views.JobAlertListView.as_view(), name='job-alert-list'),
]