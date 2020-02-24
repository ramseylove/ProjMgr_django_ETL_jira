
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib import messages
from django.http import HttpResponse


from .forms import CreateIssueForm, EditIssueForm
from .services import *


class ProjectListView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        projects = []

        for p in user.projects.all():
            project = get_project(p.p_key)
            ratio = get_issue_ratio(p.p_key)

            # project.update({'ratio': ratio})
            print(project)
            projects.append(project)

        context = {
            'projects': projects,
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

    def post(self, request, project_key, *args, **kwargs):
        form = CreateIssueForm(project_key, data=request.POST)

        if form.is_valid():
            issue = {
                'project': {'key': form.cleaned_data['project']},
                'summary': form.cleaned_data['summary'],
                'description': form.cleaned_data['description'],
                'issuetype': {'name': form.cleaned_data['issuetype']},
            }
            new_issue = create_issue(issue)
            print(new_issue)
            return redirect('issues', issue['project']['key'])
            # if new_issue:
            #     return redirect('issue-detail', project_key=issue.project['key'], issue_key=new_issue)
            # else:
            #     return render(request, 'project_manager/issue_create.html', {'form': form})


class IssueEditView(LoginRequiredMixin, View):

    def get(self, request, project_key, issue_key, *args, **kwargs):
        issue = get_issue_to_edit(project_key, issue_key)
        form = EditIssueForm(project_key, initial=issue)

        context = {
            'form': form,
        }
        return render(request, 'project_manager/issue_update.html', context)

    def post(self, request, project_key, issue_key, *args, **kwargs):
        form = EditIssueForm(project_key, data=request.POST)

        if form.is_valid():
            post_issue = {
                'summary': form.cleaned_data['summary'],
                'description': form.cleaned_data['description'],
                'issuetype': {'name': form.cleaned_data['issuetype']},
            }
            update_issue(issue_key, data=post_issue)
            if HttpResponse.status_code == 302:
                messages.add_message(request, messages.INFO, 'Post Updated')
                return redirect('issue_detail', project_key=project_key, issue_key=issue_key)
            else:
                messages.add_message(request, messages.WARNING, 'Post not updated')
                return redirect('issue_detail', project_key=project_key, issue_key=issue_key)


def fill_project_data_view(request):

    return render(request, 'project_manager/admin_project.html', {'projects': get_all_projects()})


def fill_data_view(request):

    save_projects_to_db()

    return redirect('admin_fill')
