from django.shortcuts import get_object_or_404, render
from django.views.generic import View, ListView, DetailView, CreateView

from jira import JIRA
from .models import Project, Issue
from .services import save_projects, save_all_issuetypes_to_db, save_all_issues_to_db

def load_data_view(request):

    return render(request, 'project_tracking/test.html')

def load_projects_view(request):
    projects = save_projects()

    context = {
        'projects': projects
    }

    return render(request, 'project_tracking/test.html', context)

def load_issue_types_view(request):
    issue_types = save_all_issuetypes_to_db()

    context = {
        'issue_types': issue_types
    }

    return render(request, 'project_tracking/test.html', context)

def load_issues_view(request):
    save_issues_to_db()
    issues = Issue.objects.all()

    context = {
        'issues': issues
    }

    return render(request, 'project_tracking/test.html', context)

class ProjectListView(ListView):
    model = Project
    template_name = 'project_tracking/project_list.html'
    context_object_name = 'projects'


class IssueListView(ListView):
    model = Issue
    template_name = 'project_tracking/issue_list.html'
    context_object_name = 'issues'
    
    def get_queryset(self):
        return super(IssueListView, self).get_queryset().filter(project_id=self.kwargs['project_id'])

class IssueDetailView(DetailView):
    model = Issue
    template_name = 'project_tracking/issue_detail.html'
    context_object_name = 'issue'

class IssueCreateView(View):

    def get(self, request, *args, **kwargs):
        initial = {
            'project': self.project_id
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
