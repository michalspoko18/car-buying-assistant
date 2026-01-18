from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('report/', views.report, name='report'),
    path('report/pdf/', views.report_pdf, name='report_pdf'),
]
