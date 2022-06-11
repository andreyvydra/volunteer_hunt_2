from django.urls import path
from tasks import views

urlpatterns = [
    path('create/', views.CreateTaskView.as_view(), name='task_create'),
    path('<pk>/', views.TaskView.as_view(), name='task_view'),
    path('<pk>/update', views.UpdateTaskView.as_view(), name='task_update'),
]
