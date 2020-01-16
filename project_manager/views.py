from django.shortcuts import render
from django.views.generic import View

from .jira import get_projects, get_issues, get_issue_detail

class ProjectListView(View):
    
    def get(self, request):
        
        return render(request, 'project_manager/project_list.html', {'projects': get_projects()})

class IssueListView(View):

    def get(self, request, key):

        return render(request, 'project_manager/issue_list.html', {'issues': get_issues(key) })

class IssueDetailView(View):
    
    def get(self, request, key):
            
        return render(request,'project_manager/issue_detail.html', {'issue': get_issue_detail(key)} )



