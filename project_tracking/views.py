from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, FormView


from .models import Project, Issue, IssueTypes
from .forms import CreateIssueForm, EditIssueForm
from .services import jira, create_issue, save_issue_to_db, update_issue
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class ProjectListView(ListView):
    model = Project
    template_name = 'project_tracking/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return super(ProjectListView, self).get_queryset().filter(customuser=self.request.user)


class IssueListView(ListView):
    model = Issue
    template_name = 'project_tracking/issue_list.html'
    context_object_name = 'issues'
    
    def get_queryset(self):
        return super(IssueListView, self).get_queryset().filter(project_id=self.kwargs['project_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issue_project_id'] = self.kwargs['project_id']

        return context


class IssueDetailView(DetailView):
    model = Issue
    template_name = 'project_tracking/issue_detail.html'
    context_object_name = 'issue'

# class IssueCreateView(CreateView):
#     model = Issue
#     template_name = 'project_tracking/issue_create.html'
#     fields = ['issue_type','summary','description',]
   

class IssueCreateView(View):

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
                'project': {'id': project_id }, #form.cleaned_data['project']
                'summary': form['summary'].value(),
                'description': form['description'].value(),
                'issuetype': {'id': form['issue_type'].value()},
            }
        
        new_issue = create_issue(issue)
            
        if new_issue:
            save_issue_to_db(str(new_issue.id))
            return redirect('issue_detail', pk=new_issue.id)
        else:
            return render(request, 'project_tracking/issue_create.html', {'form':form})
                
        return render(request, 'project_tracking/issue_create.html', {'form':form})
            
            
class IssueUpdateView(FormView):

    def get(self, request, *args, **kwargs):
        project_id = self.kwargs['project_id']
        issue_pk = self.kwargs['issue_pk']
        issue = Issue.objects.get(pk=issue_pk)
        form = EditIssueForm(project_id, instance=issue)

        context = {
            'form': form,
            }
        return render(request, 'project_tracking/issue_create.html', context)

    def post(self, request, *args, **kwargs):
        form = EditIssueForm(data=request.POST)

        issue = {
            'summary': form['summary'].value(),
            'description': form['description'].value(),
            'issuetype': {'id': form['issue_type'].value()},
        }

        updated_issue = update_issue(form['id'].value(), issue)

        if updated_issue && form.is_valid():
            form.save()

        HttpResponseRedirect('issue_detail', arg)


