from django.urls import path, include

from .views import (ProjectListView,
                    IssueListView,
                    IssueDetailView,
                    IssueCreateView,
                    IssueEditView,
                    fill_project_data_view,
                    fill_data_view,
                    )

urlpatterns = [
    path('projects/', ProjectListView.as_view(), name='projects'),
    path('projects/<str:key>/', IssueListView.as_view(), name='issues'),
    path('projects/<str:project_key>/issue/<str:issue_key>/', IssueDetailView.as_view(), name='issue_detail'),
    path('projects/<str:project_key>/issue/<str:issue_key>/edit/', IssueEditView.as_view(), name='issue_edit'),
    path('projects/<str:project_key>/create/', IssueCreateView.as_view(), name='issue_create'),
    path('projects/admin/fill/', fill_project_data_view, name='admin_fill'),
    path('filldata/', fill_data_view, name='fill_data'),



]
