from django.urls import path
from core import views


app_name = 'core'


urlpatterns = [
    path('', views.MainView.as_view(), name='main')
]