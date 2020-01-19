from django.conf import settings
from jira import JIRA
import arrow

from .models import Project

def jira():
    '''Connects to jira cloud
    '''
    options = {"server": settings.JIRA_URL }
    jira = JIRA(options, basic_auth=(settings.JIRA_USER, settings.JIRA_KEY))

    return jira

def get_issue_types(project_key):

    proj = jira.project(project_key)
    issue_types = proj.issueTypes

    return issue_types

def get_issue_ratio(project_key):

    proj = jira().search_issues('project = ' + project_key)
    issues = []
    total = len(proj)
    done_count = 0
    
    for issue in proj:
        issues.append({
            'status': issue.fields.status.name,
        })
    
    
    for issue in issues:
        if issue['status'] == 'Done':
            done_count += 1
        else:
            pass
        
    print('total: ' + str(total))
    print('done_count: ' + str(done_count))
    ratio = float((done_count / total) * 100) 

    return ratio

def get_project(project_key):

    project = jira().project(project_key)

    return project


def get_issues(project_key):
    
    issues = []
    proj = jira().search_issues('project = ' + project_key)
    
    for issue in proj:
        issues.append({
            'key': issue.key,
            'project': issue.fields.project,
            'status': issue.fields.status.name,
            'summary': issue.fields.summary,
            'updated_at': arrow.get(issue.fields.updated).datetime,
            'type': issue.fields.issuetype,
        })
    
    return issues


def get_issue_detail(project_key, issue_key):
    
    jira_issue = jira().issue(issue_key, fields='key,creator,created,updated,status,summary,issuetype,assignee,project')
    issue = {
        'key' : jira_issue.key,
        'creator' : jira_issue.fields.creator.displayName,
        'created_at' : arrow.get(jira_issue.fields.created).datetime,
        'updated_at' : arrow.get(jira_issue.fields.updated).datetime,
        'status' : jira_issue.fields.status.name,
        'summary' : jira_issue.fields.summary,
        'type' : jira_issue.fields.issuetype.name,
        'client' : jira_issue.fields.project.projectCategory.name
        }
    
    if jira_issue.fields.assignee:
        issue.update({'assignee':jira_issue.fields.assignee})
    else:
        issue.update({'assignee':'Not Assigned'})
    print(issue)
        
    return issue

def get_issue_basic(issue_key):

    jira_issue = jira().issue(issue_key, fields='updated')
    issue = {
        'key' : jira_issue.key,
        'updated_at' : arrow.get(jira_issue.fields.updated).datetime,
        }
        
    print(issue)
        
    return issue

def get_issues_in_project(project_key):

    issues_in_project = []
    
    proj = get_issues(project_key)
    for p in proj:
        issues_in_project.append(get_issue_detail(p.key))
        print(p)

    return issues_in_project

def create_issue(project_key):

    new_issue = jira.create_issue(
        project=project_key, 
        summary='New issue from jira-python',
        description='Look into this one', 
        issuetype=get_issue_types(project_key),
        )

    