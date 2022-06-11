from django.urls import path

from homepage import views

urlpatterns = [
    path('', views.HomepageView.as_view(), name='homepage')
]