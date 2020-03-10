from django.db import models

class Project(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    key = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=155)
    category_id = models.IntegerField(null=True,editable=False)
    category_name = models.CharField(max_length=100,null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name


class Issue(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    key = models.CharField(max_length=10)
    url = models.URLField()
    summary = models.CharField(max_length=300)
    description = models.TextField(null=True)
    status_change_date = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    status_id =  models.IntegerField()
    status_name = models.CharField(max_length=30)
    priority_id = models.IntegerField()
    priority_name = models.CharField(max_length=40)

    project = models.ForeignKey('project_tracking.Project', on_delete=models.CASCADE)
    issue_type = models.ForeignKey('project_tracking.IssueTypes', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.key


class IssueTypes(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)

    project = models.ForeignKey('project_tracking.Project', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

