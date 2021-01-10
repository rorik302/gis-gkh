from django.urls import path

from home_management import views

urlpatterns = [
    path('', views.AddressView.as_view()),
]
