
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.core.mail import send_mail

from .forms import CreateIssueForm
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

            return render(request, 'project_manager/issue_search_results.html', {'issues': issues, 'project_key': key})
        else:
            issues = get_issues(key)
            project_key = issues[0]['project']

            print(project_key)
            return render(request, 'project_manager/issue_list.html', {'issues': issues, 'project_key': project_key})


class IssueDetailView(LoginRequiredMixin, View):
    
    def get(self, request, project_key, issue_key):
            
        return render(request,'project_manager/issue_detail.html', {'issue': get_issue_detail(project_key,issue_key)})


class IssueCreateView(LoginRequiredMixin, View):

    def get(self, request, project_key, *args, **kwargs):
        initial = {
            'project': project_key,
        }

        form = CreateIssueForm(project_key, initial=initial)
        context = {'form': form}
        return render(request, 'project_manager/issue_create.html', context)

    def post(self, request, *args, **kwargs):
        form = CreateIssueForm(data=request.POST)

        if form.is_valid():
            issue = {
                'project': {'key': form.cleaned_data['project']},
                'summary': form.cleaned_data['summary'],
                'description': form.cleaned_data['description'],
                'issuetype': {'name': form.cleaned_data['issuetype']},
            }
            new_issue = create_issue(issue)
            if new_issue:
                return redirect('issue-detail', project_key=form.cleaned_data['project'], issue_key=new_issue)
            else:
                return render(request, 'project_manager/issue_create.html', {'form': form})

    # if request.method == 'POST':
    #     form = CreateIssueForm(request.post)
    #     if form.is_valid:
    #         issue = {
    #             'project': {'key': form.cleaned_data['project']},
    #             'summary': form.cleaned_data['summary'],
    #             'description': form.cleaned_data['description'],
    #             'issuetype': {'name': form.cleaned_data['issue_type']},
    #         }


class SearchResultsView(LoginRequiredMixin, View):

    def get(self, request):
        pass

        return render(request, 'project_manager/issue_search_results.html', {'issues': search_issues(query)})

