from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model

from .models import IssueTypes, Issue, Project

# def get_issue_types(project_id):
#     choices = IssueTypes.objects.get(project_id=)


class CreateIssueForm(ModelForm):

    def __init__(self, product_id, *args, **kwargs):
        super(CreateIssueForm, self).__init__(*args, **kwargs)
        self.fields['issue_type'].queryset = IssueTypes.objects.filter(project_id=product_id)

    project = forms.ModelChoiceField(
        # widget=forms.HiddenInput,
        queryset=get_user_model().projects.all(),
        disabled=True
    )

    class Meta:
        model = Issue
        fields = ['summary', 'description', 'issue_type','project']
        widgets = {
            'project': forms.HiddenInput(),
        }
    