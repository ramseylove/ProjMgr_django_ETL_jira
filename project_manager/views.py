
from django.shortcuts import render
from django.views.generic import View

from .forms import IssueForm
from .services import *

class ProjectListView(View):
    
    def get(self, request):
        user = request.user
        projects = []

        for p in user.projects.all():
            index = 0
            projects.append(get_project(p.p_key))
            ratio = get_issue_ratio(p.p_key)
            # projects[index].update({'ratio' : ratio})
            index += 1
            print(ratio)

        
        context = {
            'projects': projects,
        }
        
        return render(request, 'project_manager/project_list.html', context)

class IssueListView(View):

    def get(self, request, key):

        return render(request, 'project_manager/issue_list.html', {'issues': get_issues(key) })

class IssueDetailView(View):
    
    def get(self, request, project_key, issue_key):
            
        return render(request,'project_manager/issue_detail.html', {'issue': get_issue_detail(project_key,issue_key)})

class IssueCreateView(View):

    def get(self, request, key):
        context = {'form': IssueForm()}
        return render(request, 'project_manager/issue_create.html', context)

    # def post(self, request, project_key):
    #     form = IssueForm(request.POST)
    #     if form.is_valid():
    #         issue = form.save()
    #         issue.create


