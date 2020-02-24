from django.urls import path
from .views import home, tasks, task_detail, create_task


urlpatterns = [
    path('hubprojects/', home, name='home'),
    path('hubprojects/tasks/<str:project_id>/', tasks, name='task_list'),
    path('tasks/<str:task_id>/', task_detail, name='task_detail'),
    path('task/create/<str:project_id>/', create_task, name='create_task'),
]
