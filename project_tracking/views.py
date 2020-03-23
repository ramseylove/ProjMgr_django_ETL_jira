from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from django.views.generic import View, ListView, DetailView, CreateView



from .models import Project, Issue, IssueTypes
from .forms import CreateIssueForm
from .services import jira, create_issue, save_issue_to_db



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
            'project_id': project_id,
        }
        form = CreateIssueForm(project_id, initial=initial)
        context = {
            'form': form,
            'project': project,
            }
        return render(request, 'project_tracking/issue_create.html', context)

    def post(self, request,  *args, **kwargs):
        form = CreateIssueForm(data=request.POST)
        # project_id = self.kwargs['project_id']

        if form.is_valid():
            issue = {
                'project': {'id': form.cleaned_data['project'] },
                'summary': form.cleaned_data['summary'],
                'description': form.cleaned_data['description'],
                'issuetype': {'name': form.cleaned_data['issue_type']},
            }
            new_issue = create_issue(issue)
            
            if new_issue:
                new_issue = create_issue(issue)
                save_issue_to_db(new_issue.id)
                return HttpResponseRedirect(reverse_lazy)
            else:
                return render(request, 'project_tracking/issue_create.html', context)
                
        return render(request, 'project_tracking/issue_create.html', context)
            
            
             
            # if new_issue:
            #     return redirect('issue-detail', project_key=issue.project['key'], issue_key=new_issue)
            # else:
            #     return render(request, 'project_manager/issue_create.html', {'form': form})
