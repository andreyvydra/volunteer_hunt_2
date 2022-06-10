from django.urls import path
from tasks import views

urlpatterns = [
    path('<pk>/', views.TaskView.as_view(), name='task_view'),
]
