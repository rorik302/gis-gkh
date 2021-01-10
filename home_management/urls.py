from django.urls import path

from home_management import views


urlpatterns = [
    path('', views.AddressView.as_view()),
    path('<str:fias_id>/passport/', views.PassportPDFView.as_view(), name='passport-pdf-view')
]
