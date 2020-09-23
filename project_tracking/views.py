from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin


from .models import Project, Issue
from .forms import CreateIssueForm, EditIssueForm, AddCommentForm
from .services import create_issue, save_issue_to_db, update_issue, get_comments


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'project_tracking/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return super(ProjectListView, self).get_queryset().filter(customuser=self.request.user)


class IssueListView(LoginRequiredMixin, ListView):
    model = Issue
    template_name = 'project_tracking/issue_list.html'
    context_object_name = 'issues'
    
    def get_queryset(self):
        return super(IssueListView, self).get_queryset().filter(project_id=self.kwargs['project_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issue_project_id'] = self.kwargs['project_id']
        context['project'] = Project.objects.get(id=self.kwargs['project_id'])

        return context


class IssueDetailView(LoginRequiredMixin, DetailView):
    model = Issue
    template_name = 'project_tracking/issue_detail.html'
    context_object_name = 'issue'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = get_comments(self.kwargs['pk'])
        context['form'] = AddCommentForm()

        return context


class AddCommentView(FormView):
    # TODO: need an form view to include on issue detail page
    form_class = AddCommentForm
   

class IssueCreateView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        project_id = self.kwargs['project_id']
        project = Project.objects.get(id=project_id)
        initial = {
            'project': project,
        }
        form = CreateIssueForm(request, project_id, initial=initial)
        context = {
            'form': form,
            'project': project,
            }
        return render(request, 'project_tracking/issue_create.html', context)

    def post(self, request,  *args, **kwargs):
        project_id = self.kwargs['project_id']
        form = CreateIssueForm(request, project_id, data=request.POST)

        issue = {
                'project': {'id': project_id },
                'summary': form['summary'].value(),
                'description': form['description'].value(),
                'issuetype': {'id': form['issue_type'].value()},
            }
        
        new_issue = create_issue(issue)
            
        if new_issue:
            save_issue_to_db(str(new_issue.id))
            messages.success(request, "New issue has been created")
            return redirect('issue_detail', pk=new_issue.id)
        else:
            messages.error(request, "Issue was not created, Please correct any issue")
            return render(request, 'project_tracking/issue_create.html', {'form': form})

            
class IssueUpdateView(LoginRequiredMixin, FormView):

    def get(self, request, *args, **kwargs):
        project_id = self.kwargs['project_id']
        issue_pk = self.kwargs['issue_pk']
        issue = Issue.objects.get(pk=issue_pk)
        form = EditIssueForm(project_id, instance=issue)

        context = {
            'form': form,
            'issue': issue,
            }
        return render(request, 'project_tracking/issue_update.html', context)

    def post(self, request, *args, **kwargs):
        project_id = self.kwargs['project_id']
        project = Project.objects.get(id=project_id)
        issue_pk = self.kwargs['issue_pk']
        issue = Issue.objects.get(pk=issue_pk)
        form = EditIssueForm(project_id, data=request.POST, instance=issue)

        new_issue = {
            'summary': form['summary'].value(),
            'description': form['description'].value(),
            'issuetype': {'id': form['issue_type'].value()},
        }

        updated_issue = update_issue(issue_pk, new_issue)
        print(updated_issue)

        if updated_issue:
            return redirect('issue_detail', pk=issue_pk)
        else:
            return render(request, 'project_tracking/issue_create.html', {'form': form})

        return render(request, 'project_tracking/issue_create.html', {'form': form})

