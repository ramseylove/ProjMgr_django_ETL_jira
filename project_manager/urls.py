from django.urls import path

from .views import ProjectListView, IssueListView, IssueDetailView

urlpatterns = [
    path('projects/', ProjectListView.as_view(), name='projects'),
    path('projects/<str:key>/', IssueListView.as_view(), name='issues'),
    path('projects/issue/<str:key>/', IssueDetailView.as_view(), name='issue_detail'),

]
