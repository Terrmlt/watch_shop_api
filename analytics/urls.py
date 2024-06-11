from django.urls import path

from analytics import views

app_name = 'analytics'

urlpatterns = [
    path(r'analytics/summary', views.summary, name='summary'),
    path(r'analytics/status', views.status, name='status'),
]
