from django.db import models

class Project(models.Model):
    id = models.IntegerField(primary_key=True, max_length=20, unique=True)
    key = models.CharField(primary_key=True, max_length=20, unique=True)
    name = models.CharField(max_length=155)
    category_id = models.IntegerField(max_length=20)
    category_name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Issue(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, max_length=20)
    key = models.CharField(max_length=10)
    summary = models.Charfield(max_length=300)
    description = models.TextField()
    status_change_date = models.DateTimeField
    created_at = models.DateTimeField
    updated_at = models.DateTimeField
    status =  models.CharField(max_length=30)

    project_id = models.ForeignKey("Project", on_delete=models.CASCADE))
    issue_type_id = models.ForeignKey("IssueTypes", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class IssueTypes(models.Model):
    id = models.IntegerField(primary_key=True, unique=true, max_length=20)
    name = models.CharField(max_length=100)

    project_id = models.ForeignKey("Project", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

