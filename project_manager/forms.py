from django import forms

# from .views import IssueCreateView

class IssueForm(forms.Form):
    project = forms.CharField()
    summary = forms.CharField(max_length=255, help_text='Summary of issue')
    description = forms.TextInput()
    issue_type = forms.ChoiceField()