from django import forms
from django.forms import ModelForm

from .models import IssueTypes, Issue, IssueImages


class CreateIssueForm(ModelForm):

    def __init__(self, request, project_id, *args, **kwargs):
        super(CreateIssueForm, self).__init__(*args, **kwargs)
        user = request.user
        self.fields['issue_type'].queryset = IssueTypes.objects.filter(project_id=project_id)
        self.fields['project'].queryset = user.projects.all()
        self.fields['project'].disabled = True

    class Meta:
        model = Issue
        fields = ['project', 'summary', 'description', 'issue_type']


class EditIssueForm(ModelForm):

    def __init__(self, project_id, *args, **kwargs):
        super(EditIssueForm, self).__init__(*args, **kwargs)
        self.fields['issue_type'].queryset = IssueTypes.objects.filter(project_id=project_id)
        self.fields['project'].disabled = True

    class Meta:
        # TODO : hide Project selection drop down menu
        model = Issue
        fields = ['issue_type', 'project', 'summary', 'description', ]


class ImageForm(ModelForm):
    image = forms.ImageField(label='Screenshot')

    class Meta:
        model = IssueImages
        fields = ('image', )

class AddCommentForm(forms.Form):
    comment = forms.CharField(label='Add Comment', max_length=255)

