from django.conf import settings
from IPython.core.debugger import set_trace
import pandas as pd
from pandas import json_normalize
from psqlextra.query import ConflictAction
import requests
from jira import JIRA
from .models import Project, Issue, IssueTypes


BASE_URL = 'https://atriadev.atlassian.net/rest/api/3/'
TOKEN = settings.JIRA_KEY
USER = settings.JIRA_USER

def jira():
    """
    Connects to jira cloud returns connection
    """
    options = {"server": settings.JIRA_URL }
    j = JIRA(options, basic_auth=(settings.JIRA_USER, settings.JIRA_KEY))

    return j

def get_projects():
    url = BASE_URL + 'project/search'
    
    payload = { 
        'expand': ['issueTypes','insight'],
        }
    
    r = requests.get(url, auth=(USER, TOKEN), params=payload)
    r = r.json()
    r = r['values']

    return r


def update_projects_in_db():
    projects = get_projects()
    projects_df = json_normalize(projects)
    projects_df = projects_df[['id','key','name','projectCategory.name','projectCategory.id','projectCategory.description']]
    projects_df = projects_df.where(pd.notnull(projects_df), None)

    db_keys = Project.objects.values_list('key', flat=True)
    update_projects_df = projects_df[projects_df[projects_df.columns[1]].isin(db_keys)]
    create_projects_df = projects_df[~projects_df[projects_df.columns[1]].isin(db_keys)]
    print(update_projects_df)
    print(create_projects_df)

    def dataframe_assignment(df):
        
        records = df.to_dict('records')
        instances = [Project(
            id = int(record['id']),
            key = record['key'],
            name = record['name'],
            category_id = record['projectCategory.id'],
            category_name = record['projectCategory.name'],
            description = record['projectCategory.description']
        ) for record in records]
        
        return instances

    fields = [
        'key',
        'name',
        'category_id',
        'category_name',
        'description',
    ]

    Project.objects.bulk_update(dataframe_assignment(update_projects_df), fields, batch_size=50)
    Project.objects.bulk_create(dataframe_assignment(create_projects_df))
    

def update_all_issuetypes_to_db():
    projects = get_projects()

    issue_types_df = json_normalize(data=projects, record_path='issueTypes', meta=['id'], meta_prefix='project_' )
    issue_types_df = issue_types_df.set_index("id", drop = False)
    issue_types_df = issue_types_df[['id','name','project_id']]

    db_ids = IssueTypes.objects.values_list('id', flat=True)
    update_issue_types_df = issue_types_df[issue_types_df[issue_types_df.columns[0]].isin(db_ids)]
    create_issue_types_df = issue_types_df[~issue_types_df[issue_types_df.columns[0]].isin(db_ids)]
    print(update_issue_types_df)
    print(create_issue_types_df)

    def dataframe_assignment(df):
        records = df.to_dict('records')
        instances = [IssueTypes(
            id = int(record['id']),
            name = record['name'],
            project = Project.objects.get(id=int(record['project_id']))

        ) for record in records]
        
        return instances

    fields = [
        'name',
        'project',
    ]
    
    IssueTypes.objects.bulk_update(dataframe_assignment(update_issue_types_df), fields, batch_size=50)
    IssueTypes.objects.bulk_create(dataframe_assignment(create_issue_types_df))


def get_all_project_ids():

    project_list = Project.objects.all().values('id')
    id_list = []
    for id in project_list:
        id_list.append(id['id'])

    ids = str(id_list).strip('[]')

    return ids
      

def get_issues(ids):
    '''Make the intial query'''
    def make_query(ids, max_results=100, start_at=0):
        
        url = BASE_URL + 'search'
    
        query = {
            'jql': 'project in ({})'.format(ids),
            'fields': [
                'id','self','key','summary','statuscategorychangedate',
                'issuetype','description','priority','project', 'status','created','updated'],
            'maxResults': max_results,
            'startAt': start_at,
            }

        r = requests.get(url, auth=(USER, TOKEN), params=query)
        r = r.json()
        
        return r
    
    results = make_query(ids)
    
    total = results['total']
    issues = results['issues']
    
    if total > 100:
        paged_results = 0
        total_results = (total - 100)
        
        while total_results > 100:
            paged_results += 100
            results = make_query(ids, start_at=paged_results)
            issues.extend(results['issues'])
            total_results -= 100
            print(len(issues))
        else:
            paged_results += 100
            results = make_query(ids, max_results=total_results, start_at=paged_results)
            issues.extend(results['issues'])
            print(len(issues))


    issues_df = json_normalize(data=issues, max_level=1, sep='_')
    issues_df = issues_df.set_index("id", drop = False)
    issues_df = issues_df.where(pd.notnull(issues_df), None)

    return issues_df


def update_all_issues_to_db():
    proj_ids = get_all_project_ids()
    issues_df = get_issues(proj_ids)

    db_ids = Issue.objects.values_list('id', flat=True)
    update_issues_df = issues_df[issues_df[issues_df.columns[1]].isin(db_ids)]
    create_issues_df = issues_df[~issues_df[issues_df.columns[1]].isin(db_ids)]

    def dataframe_assignment(df):
        records= df.to_dict('records')
        instances = [Issue(
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

            project = Project.objects.get(id=int(record['fields_project']['id'])),
            issue_type = IssueTypes.objects.get(id=int(record['fields_issuetype']['id'])),
        ) for record in records] 

        return instances
    
    fields = [
        'key',
        'url',
        'summary',
        'description',
        'status_change_date',
        'created_at',
        'updated_at',
        'status_id',
        'status_name',
        'priority_id',
        'priority_name',
        'project',
        'issue_type', 
    ]

    Issue.objects.bulk_update(dataframe_assignment(update_issues_df), fields, batch_size=50)
    Issue.objects.bulk_create(dataframe_assignment(create_issues_df))



def add_issue_to_jira():
    pass


def get_issue(id):
    url = BASE_URL + 'issue/' + int(id)
    
    r = requests.get(url, auth=(USER, TOKEN))
    r = r.json()

    return r


def save_issue_to_db(id):
    issue = get_issue(id)

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

def create_issue(issue):

    new_issue = jira().create_issue(fields=issue)
    print(new_issue)

    return new_issue

    