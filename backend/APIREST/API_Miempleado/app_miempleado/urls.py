from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register),
    path('sign-in/', views.sign_in),
    path('sign-out/', views.sign_out),
    path('holidays-absences/', views.holidaysNabsences)
]
