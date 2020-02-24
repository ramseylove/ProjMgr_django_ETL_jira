from django.shortcuts import render, reverse
from .services import *



def home(request):
    token = get_access_token()
    print(token)
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + token['access_token']}
    print(headers)
    expiry = token['expires_in']
    request.session['access_token'] = headers
    # request.session.set_expiry(int(expiry))

    
    proj = get_projects(headers)
    print(proj)

    # context = {
    #     'proj': proj
    # }

    return render(request, 'tasks/home.html', {'proj':proj})

def tasks(request, project_id):
    
    headers = request.session['access_token']

    tasks = get_tasks_for_project(headers, project_id)

    context = {
        'tasks': tasks,
        'project_id': project_id
    }

    return render(request, 'tasks/tasks.html', context)

def task_detail(request, task_id):

    headers = request.session['access_token']

    task = get_task(headers, task_id)

    return render(request, 'tasks/task.html', {'task':task})

def create_task(request, project_id):
    headers = request.session['access_token']
    
    new_task = {
        'summary': 'test summary123435251',
        'assignee_id': 666788
    }
    task = save_task(headers, project_id, new_task)
    print(task)

    return render(request, 'tasks/create_task.html')
