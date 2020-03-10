from django.conf import settings
import pandas as pd
from pandas import json_normalize
import requests

from .models import Project, Issue, IssueTypes


BASE_URL = 'https://atriadev.atlassian.net/rest/api/3/'
TOKEN = settings.JIRA_KEY
USER = settings.JIRA_USER


def get_projects():
    url = BASE_URL + 'project/search'
    
    payload = { 
        'expand': ['issueTypes','insight'],
        }
    
    r = requests.get(url, auth=(USER, TOKEN), params=payload)
    r = r.json()
    r = r['values']

    return r

def save_projects():
    projects = get_projects()
    projects_df = json_normalize(projects)
    projects_df = projects_df[['id','key','name','projectCategory.name','projectCategory.id','projectCategory.description']]
    projects_df = projects_df.where(pd.notnull(projects_df), None)
    projects_dict = projects_df.to_dict('records')
    print(projects_dict)
    
    issue_types = json_normalize(data=projects, record_path='issueTypes', meta=['id'], meta_prefix='project_' )
    issue_types_dataframe = issue_types[['id','name','subtask','project_id']]
    issue_types_dict = issue_types_dataframe.to_dict('records')

    project_instances = [Project(
        id = int(record['id']),
        key = record['key'],
        name = record['name'],
        category_id = record['projectCategory.id'],
        category_name = record['projectCategory.name'],
        description = record['projectCategory.description']
    ) for record in projects_dict]

    fields = [
        'key',
        'name',
        'category_id',
        'category_name',
        'description',
    ]
    updates = Project.objects.all().in_bulk()

    if hasattr(project_instances, 'bulk_update') and updates:
        Project.objects.bulk_update(updates.values(), fields, batch_size=50)
    


def save_all_issuetypes_to_db():
    projects = get_projects()

    issue_types = json_normalize(data=projects, record_path='issueTypes', meta=['id'], meta_prefix='project_' )
    issue_types_dataframe = issue_types[['id','name','subtask','project_id']]
    issue_types_dict = issue_types_dataframe.to_dict('records')

    issue_type_instances = [IssueTypes(
        id = int(record['id']),
        name = record['name'],
        project = Project.objects.get(id=int(record['project_id']))

    ) for record in issue_types_dict]

    IssueTypes.objects.bulk_create(issue_type_instances)


def get_all_issues():
    url = BASE_URL + 'search'

    project_list = Project.objects.all().values('id')
    id_list = []
    for id in project_list:
        id_list.append(id['id'])

    ids = str(id_list).strip('[]')
    
    query = {
        'jql': 'project in ({})'.format(ids),
        'fields': [
            'id','self','key','summary','statuscategorychangedate',
            'issuetype','description','priority','project', 'status','created','updated']
        }
    
    r = requests.get(url, auth=(USER, TOKEN), params=query)
    r = r.json()
    r = r['issues']

    return r

def save_issues_to_db():
    issues = get_all_issues()

    issues_flattened = json_normalize(data=issues, max_level=1, sep='_')
    issues_flattened.where(pd.notnull(issues_flattened), None)
    issues_flattened_dict = issues_flattened.to_dict('records')

    issue_instances = [Issue(
        id = int(record['id']),
        key = record['key'],
        url = record['self'],
        summary = record['fields_summary'],
        description = record['fields_description'],
        status_change_date = record['fields_statuscategorychangedate'],
        created_at = record['fields_created'],
        updated_at = record['fields_updated'],
        status_id = record['fields_status']['id'],
        status_name = record['fields_status']['name'],
        priority_id = record['fields_priority']['id'],
        priority_name = record['fields_priority']['name'],

        project= Project.objects.get(id=int(record['fields_project']['id'])),
        issue_type = IssueTypes.objects.get(id=int(record['fields_issuetype']['id'])),
    ) for record in issues_flattened_dict] 

    Issue.objects.bulk_create(issue_instances)

def add_issue_to_jira():
    pass


def get_issue(id):
    url = BASE_URL + 'issue/' + str(id)
    
    r = requests.get(url, auth=(USER, TOKEN))
    r = r.json()

    return r


def save_issue_to_db(issue):
    issue = get_issue()

    issue_flattened = json_normalize(data=issue, max_level=1, sep='_')
    issue_flattened.where(pd.notnull(issue_flattened), None)
    issue_flattened_dict = issues_flattened.to_dict('records')

    issue_instance = Issue(
        id = int(record['id']),
        key = record['key'],
        url = record['self'],
        summary = record['fields_summary'],
        description = record['fields_description'],
        status_change_date = record['fields_statuscategorychangedate'],
        created_at = record['fields_created'],
        updated_at = record['fields_updated'],
        status_id = record['fields_status']['id'],
        status_name = record['fields_status']['name'],
        priority_id = record['fields_priority']['id'],
        priority_name = record['fields_priority']['name'],

        project= Project.objects.get(id=int(record['fields_project']['id'])),
        issue_type = IssueTypes.objects.get(id=int(record['fields_issuetype']['id'])),
    )

    Issue.object.create(issue_instance)

    