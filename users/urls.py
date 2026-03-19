from django.urls import path
from . import views

urlpatterns = [
    path('registeration/', views.RegistrationAPIew.as_view()),
    path('authorization/', views.AuthorizationAPIew.as_view()),
    path('confirm/', views.UserConfirmView.as_view()),
]