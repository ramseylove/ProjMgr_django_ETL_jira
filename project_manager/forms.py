from django import forms

from .services import get_issue_types


class CreateIssueForm(forms.Form):
    def __init__(self, project_key, *args, **kwargs):
        super(CreateIssueForm, self).__init__(*args, **kwargs)
        self.fields['issuetype'] = forms.ChoiceField(choices=get_issue_types(project_key))

    project = forms.CharField(max_length=10, widget=forms.HiddenInput, required=True)
    summary = forms.CharField(max_length=150, label='Summary', help_text='Summary of issue')
    description = forms.CharField(max_length=600, help_text='Describe the issue', widget=forms.Textarea, required=False)
    issuetype = forms.ChoiceField()
