from django.urls import path

from .views import ProjectListView, IssueListView, IssueDetailView, IssueCreateView, SearchResultsView

urlpatterns = [
    path('projects/', ProjectListView.as_view(), name='projects'),
    path('projects/<str:key>/', IssueListView.as_view(), name='issues'),
    path('projects/<str:project_key>/issue/<str:issue_key>/', IssueDetailView.as_view(), name='issue_detail'),
    path('projects/<str:key>/issue/create/', IssueCreateView.as_view(), name='issue_create'),
    path('projects/search/', SearchResultsView.as_view(), name='search_results'),


]
