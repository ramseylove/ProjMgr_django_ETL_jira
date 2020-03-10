from django import forms

from .models import IssueTypes

def get_issue_types(project_id):

class CreateIssueForm(forms.Form):

    def __init__(self, project_key, *args, **kwargs):
        super(CreateIssueForm, self).__init__(*args, **kwargs)
        self.fields['issue_type'] = forms.ChoiceField(choices=self.issue_type)

    project = forms.CharField(max_length=10, widget=forms.HiddenInput, required=True)
    summary = forms.CharField(max_length=150, label='Summary', help_text='Summary of issue')
    description = forms.CharField(max_length=600, help_text='Describe the issue', widget=forms.Textarea, required=False)
    issuetype = forms.ChoiceField()