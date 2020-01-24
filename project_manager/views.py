
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View

from .forms import IssueForm
from .services import *

class ProjectListView(LoginRequiredMixin, View):
    
    def get(self, request):
        user = request.user
        projects = []

        for p in user.projects.all():
            project = get_project(p.p_key)
            ratio = get_issue_ratio(p.p_key)

            projects.append(project)
        
        context = {
            'projects': projects,
            'ratio': ratio,
        }
        
        return render(request, 'project_manager/project_list.html', context)

class IssueListView(LoginRequiredMixin, View):

    def get(self, request, key):
        
        if 'query' in request.GET:
            query = request.GET['query']
            print(query)
            issues = get_issues(key, query)

            return render(request, 'project_manager/issue_search_results.html', {'issues': issues })
        else:
            return render(request, 'project_manager/issue_list.html', {'issues': get_issues(key) })

class IssueDetailView(LoginRequiredMixin, View):
    
    def get(self, request, project_key, issue_key):
            
        return render(request,'project_manager/issue_detail.html', {'issue': get_issue_detail(project_key,issue_key)})

class IssueCreateView(LoginRequiredMixin, View):

    def get(self, request, key):
        context = {'form': IssueForm()}
        return render(request, 'project_manager/issue_create.html', context)

    # def post(self, request, project_key):
    #     form = IssueForm(request.POST)
    #     if form.is_valid():
    #         issue = form.save()
    #         issue.create

class SearchResultsView(LoginRequiredMixin, View):

    def get(self, request):
        pass

        return render(request, 'project_manager/issue_search_results.html', {'issues': search_issues(query)})

