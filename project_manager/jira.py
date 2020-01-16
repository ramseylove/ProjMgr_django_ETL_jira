from django.conf import settings
from jira import JIRA
import arrow

def jira():

    options = {"server": settings.JIRA_URL }
    jira = JIRA(options, basic_auth=(settings.JIRA_USER, settings.JIRA_KEY))

    return jira


def get_projects():
    
    projects = jira().projects()
    project_list = []
    
    for project in projects:
        
        project_list.append({
            'key' : project.key,
            'name' : project.name,
            'last_updated' : arrow.get(project.fields.lastIssueUpdateTime),
        })
    print(project_list)
    
    return project_list


def get_issues(project_key):
    
    issues_in_project = jira().search_issues('project=' + project_key)
    print(len(issues_in_project))

    return issues_in_project


def get_issue_detail(issue_key):
    
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

    