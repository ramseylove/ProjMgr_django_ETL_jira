from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model

from .models import IssueTypes, Issue, Project

# def get_issue_types(project_id):
#     choices = IssueTypes.objects.get(project_id=)
UserModel = get_user_model()


class CreateIssueForm(ModelForm):

    def __init__(self, request, project_id, *args, **kwargs):
        super(CreateIssueForm, self).__init__(*args, **kwargs)
        user = request.user
        self.fields['issue_type'].queryset = IssueTypes.objects.filter(project_id=project_id)
        self.fields['project'].queryset = user.projects.all()

    class Meta:
        model = Issue
        fields = ['project','summary', 'description', 'issue_type']


class EditIssueForm(ModelForm):

    def __init__(self, project_id, *args, **kwargs):
        super(EditIssueForm, self).__init__(*args, **kwargs)
        self.fields['issue_type'].queryset = IssueTypes.objects.filter(project_id=project_id)

    class Meta:
        model = Issue
        fields = ['id', 'project', 'summary', 'description', 'issue_type']
    