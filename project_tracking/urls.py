from django.urls import path, include

from .views import (ProjectListView,
                    IssueListView,
                    IssueDetailView,
                    IssueCreateView,
                    IssueUpdateView)
    


urlpatterns = [
    path('project_tracking/', ProjectListView.as_view(), name='project_list'),
    path('project_tracking/<int:project_id>/', IssueListView.as_view(), name='issue_list'),
    path('project_tracking/issue/<int:pk>/', IssueDetailView.as_view(), name='issue_detail'),
    path('project_tracking/<int:project_id>/createissue', IssueCreateView.as_view(), name='issue_create'),
    path('project_tracking/<int:project_id>/updateissue/<int:issue_pk>/', IssueUpdateView.as_view(), name='issue_update'),

]
