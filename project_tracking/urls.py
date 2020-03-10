from django.urls import path, include

from .views import (load_data_view, 
                    load_issues_view, 
                    load_issue_types_view, 
                    load_projects_view, 
                    ProjectListView,
                    IssueListView,
                    IssueDetailView)
    


urlpatterns = [
    path('project_tracking_data/', load_data_view, name='load_data'),
    path('project_tracking_data/load_issues/', load_issues_view, name='load_issues'),
    path('project_tracking_data/load_issue_types/', load_issue_types_view, name='load_issue_types'),
    path('project_tracking_data/load_projects/', load_projects_view, name='load_projects'),
    path('project_tracking/', ProjectListView.as_view(), name='project_list'),
    path('project_tracking/<int:project_id>/', IssueListView.as_view(), name='issue_list'),
    path('project_tracking/issue/<int:pk>/', IssueDetailView.as_view(), name='issue_detail'),
]
