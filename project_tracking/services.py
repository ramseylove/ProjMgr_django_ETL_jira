import arrow
from django.conf import settings
import pandas as pd
from pandas import json_normalize
import requests
from jira import JIRA
from .models import Project, Issue, IssueTypes, IssueImages
from django.db import DatabaseError

BASE_URL = 'https://atriadev.atlassian.net/rest/api/2/'
TOKEN = settings.JIRA_KEY
USER = settings.JIRA_USER


def jira():
    """
    Connects to jira cloud returns connection
    """
    options = {"server": settings.JIRA_URL}
    j = JIRA(options, basic_auth=(settings.JIRA_USER, settings.JIRA_KEY))

    return j


def get_projects():
    url = BASE_URL + 'project/search'

    payload = {
        'expand': ['issueTypes', 'insight'],
    }

    r = requests.get(url, auth=(USER, TOKEN), params=payload)
    r = r.json()
    r = r['values']

    return r


def update_projects_in_db(projects):
    projects_df = json_normalize(projects)
    projects_df = projects_df[
        ['id', 'key', 'name', 'projectCategory.name', 'projectCategory.id', 'projectCategory.description']]
    projects_df = projects_df.where(pd.notnull(projects_df), None)

    db_keys = Project.objects.values_list('key', flat=True)
    update_projects_df = projects_df[projects_df[projects_df.columns[1]].isin(db_keys)]
    create_projects_df = projects_df[~projects_df[projects_df.columns[1]].isin(db_keys)]

    def dataframe_assignment(df):

        records = df.to_dict('records')
        instances = [Project(
            id=int(record['id']),
            key=record['key'],
            name=record['name'],
            category_id=record['projectCategory.id'],
            category_name=record['projectCategory.name'],
            description=record['projectCategory.description']
        ) for record in records]

        return instances

    fields = [
        'key',
        'name',
        'category_id',
        'category_name',
        'description',
    ]
    if not create_projects_df.empty:
        Project.objects.bulk_create(dataframe_assignment(create_projects_df))
        print('New Projects Created')
    try:
        Project.objects.bulk_update(dataframe_assignment(update_projects_df), fields, batch_size=50)
    except DatabaseError:
        print('There was an issue while updating projects')


def update_all_issuetypes_to_db(projects):
    issue_types_df = json_normalize(data=projects, record_path='issueTypes', meta=['id'], meta_prefix='project_')
    issue_types_df = issue_types_df.set_index("id", drop=False)
    issue_types_df = issue_types_df[['id', 'name', 'project_id']]

    db_ids = IssueTypes.objects.values_list('id', flat=True)
    create_issue_types_df = issue_types_df[~issue_types_df[issue_types_df.columns[0]].isin(db_ids)]
    update_issue_types_df = issue_types_df[issue_types_df[issue_types_df.columns[0]].isin(db_ids)]

    def dataframe_assignment(df):
        records = df.to_dict('records')
        instances = [IssueTypes(
            id=int(record['id']),
            name=record['name'],
            project=Project.objects.get(id=int(record['project_id']))

        ) for record in records]

        return instances

    fields = [
        'name',
        'project',
    ]
    if not create_issue_types_df.empty:
        IssueTypes.objects.bulk_create(dataframe_assignment(create_issue_types_df))
        print('New Issue Types Added')
    try:
        IssueTypes.objects.bulk_update(dataframe_assignment(update_issue_types_df), fields, batch_size=50)
        return 'IssueTypes updated Succesfully'
    except DatabaseError:
        print('There was an issue while updating projects')


def get_all_project_ids():
    project_list = Project.objects.all().values('id')
    id_list = []
    for id in project_list:
        id_list.append(id['id'])

    ids = str(id_list).strip('[]')

    return ids


def get_all_issues():
    '''Make the intial query'''
    proj_ids = get_all_project_ids()

    def make_query(project_ids, max_results=100, start_at=0):

        url = BASE_URL + 'search'

        query = {
            'jql': 'project in ({})'.format(project_ids),
            'fields': [
                'id', 'self', 'key', 'summary', 'statuscategorychangedate',
                'issuetype', 'description', 'priority', 'project', 'status', 'created', 'updated', 'attachment'],
            'maxResults': max_results,
            'startAt': start_at,
        }

        r = requests.get(url, auth=(USER, TOKEN), params=query)
        r = r.json()

        return r

    results = make_query(proj_ids)

    total = results['total']
    issues = results['issues']

    if total > 100:
        paged_results = 0
        total_results = (total - 100)

        while total_results > 100:
            paged_results += 100
            results = make_query(proj_ids, start_at=paged_results)
            issues.extend(results['issues'])
            total_results -= 100
            print(len(issues))
        else:
            paged_results += 100
            results = make_query(proj_ids, max_results=total_results, start_at=paged_results)
            issues.extend(results['issues'])
            print(len(issues))

    return issues


def save_all_issues_to_db(issues):
    issues_df = json_normalize(data=issues, max_level=1, sep='_')
    issues_df = issues_df.set_index("id", drop=False)
    issues_df = issues_df.where(pd.notnull(issues_df), None)

    db_issue_ids = Issue.objects.values_list('id', flat=True)
    create_issues_df = issues_df[~issues_df[issues_df.columns[1]].isin(db_issue_ids)]
    update_issues_df = issues_df[issues_df[issues_df.columns[1]].isin(db_issue_ids)]

    def issue_assignment(df):
        records = df.to_dict('records')
        instances = [Issue(
            id=int(record['id']),
            key=record['key'],
            url=record['self'],
            summary=record['fields_summary'],
            description=record['fields_description'],
            status_change_date=record['fields_statuscategorychangedate'],
            created_at=record['fields_created'],
            updated_at=record['fields_updated'],
            status_id=record['fields_status']['id'],
            status_name=record['fields_status']['name'],
            priority_id=record['fields_priority']['id'],
            priority_name=record['fields_priority']['name'],

            project=Project.objects.get(id=int(record['fields_project']['id'])),
            issue_type=IssueTypes.objects.get(id=int(record['fields_issuetype']['id'])),

        ) for record in records]

        return instances

    issue_fields = [
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

    if not create_issues_df.empty:
        Issue.objects.bulk_create(issue_assignment(create_issues_df))
        print('New issues created')
    try:
        Issue.objects.bulk_update(issue_assignment(update_issues_df), issue_fields, batch_size=50)
    except DatabaseError:
        print('Something went wrong with updating')


def save_all_issueimages_to_db(issues):
    attachment_df = json_normalize(data=issues, record_path=[['fields', 'attachment']], meta=['id'],
                                   meta_prefix='issue_', sep='_')
    attachment_df = attachment_df.set_index("id", drop=False)
    print(attachment_df)

    db_issueimage_ids = IssueImages.objects.values_list('id', flat=True)
    update_issueimages_df = attachment_df[attachment_df[attachment_df.columns[1]].isin(db_issueimage_ids)]
    create_issueimages_df = attachment_df[~attachment_df[attachment_df.columns[1]].isin(db_issueimage_ids)]

    def issue_images_assignment(df):
        records = df.to_dict('records')
        instances = [IssueImages(
            id=int(record['id']),
            filename=record['filename'],
            content=record['content'],
            thumbnail=record['thumbnail'],

            issue=Issue.objects.get(id=int(record['issue_id']))
        ) for record in records]

        return instances

    image_fields = [
        'filename',
        'content',
        'thumbnail',
        'issue',
    ]
    if not create_issueimages_df.empty:
        IssueImages.objects.bulk_create(issue_images_assignment(create_issueimages_df))
        print('New images added')

    try:
        IssueImages.objects.bulk_update(issue_images_assignment(update_issueimages_df), image_fields, batch_size=50)
        print('Images update Succesfully')
    except DatabaseError:
        print('There was an issue with updating images')


def update_all_issues_to_db():
    issues = get_all_issues()

    save_all_issues_to_db(issues)
    save_all_issueimages_to_db(issues)


def get_issue(issue_id):
    url = BASE_URL + 'issue/' + str(issue_id)

    r = requests.get(url, auth=(USER, TOKEN))
    r = r.json()

    return r


def save_issue_to_db(issue_id):
    issue = get_issue(issue_id)

    issue_flattened = json_normalize(data=issue, max_level=1, sep='_')
    issues_flattened = issue_flattened.where(pd.notnull(issue_flattened), None)
    record = issues_flattened.to_dict('records')
    record = record[0]

    issue_instance = Issue(
        id=int(record['id']),
        key=record['key'],
        url=record['self'],
        summary=record['fields_summary'],
        description=record['fields_description'],
        status_change_date=record['fields_statuscategorychangedate'],
        created_at=record['fields_created'],
        updated_at=record['fields_updated'],
        status_id=record['fields_status']['id'],
        status_name=record['fields_status']['name'],
        priority_id=record['fields_priority']['id'],
        priority_name=record['fields_priority']['name'],

        project=Project.objects.get(id=int(record['fields_project']['id'])),
        issue_type=IssueTypes.objects.get(id=int(record['fields_issuetype']['id'])),
    ).save()


def create_issue(issue):
    new_issue = jira().create_issue(fields=issue)
    print(new_issue)

    return new_issue


def update_issue(issue_key, data):
    jira_issue = jira().issue(issue_key)
    print(jira_issue)

    if jira_issue:
        jira_issue.update(fields=data)
        save_issue_to_db(issue_key)
        return True
    else:
        return False


def get_issue_comments(issue_id):
    issue = jira().issue(issue_id)
    comments = jira().comments(issue)

    return comments


def get_comments(issue_id):
    comment_list = []
    comments = get_issue_comments(issue_id)
    for c_id in comments:
        comment = jira().comment(issue_id, c_id)

        comment_dict = {
            "id": comment.id,
            "author": comment.author.displayName,
            "body": comment.body,
            "created": arrow.get(comment.created).datetime,
            "human_date": arrow.get(comment.created).humanize(),
            "url": comment.self

        }
        comment_list.append(comment_dict)

    return comment_list


def add_comment(issue_id):
    # TODO: create service to add comment from add comment form

    return None