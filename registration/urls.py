from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name='home'),
    path('form/', views.form_view, name='form'),
    path('parse_resume/', views.parse_resume, name='parse_resume'),
    path('success/', views.success, name='success'),
]
