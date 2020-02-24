from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import TokenExpiredError

import arrow
import json
import requests

ORG_ID = '195167'
BASE_URL = 'https://api.hubstaff.com/v2/'
CLIENT_ID = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6ImRlZmF1bHQifQ.eyJqdGkiOiJVRktFZzhrUCIsImlzcyI6Imh0dHBzOi8vYWNjb3VudC5odWJzdGFmZi5jb20iLCJleHAiOjE1ODk1ODUxMzYsImlhdCI6MTU4MTgxMjczNiwic2NvcGUiOiJvcGVuaWQgaHVic3RhZmY6cmVhZCBodWJzdGFmZjp3cml0ZSJ9.iNrzZHnXLcm9Yn9YioXYxwbdzhpL-70SFS9QGjHkx1A-NDEecl0i-BjILaHzIFsUJJRgb5g4mtQWfK4DYs7GTKdnFahIoKwxa5XHVVOHXmV3vOUJmUe4aQqBV51dQ-2CXBShbU_d1M74uLY5d2n2xZwELttIv7joOOT20JtdRGvmVtMngkzCHYKWNCCej16HqbkZ_ecTBlXzXoJ0GNR_MZRqLY6RIlbjD6BUA9GQzVGBfrQMVh4ft472nNwhNT36FXpKsI-Ho-UKq0vhvBBz_bUsTcwc6SKlso2p4MlqgYMx4zYjWT6Hi1ib1IGdzhCH4h0XGxH8L_PDCYiqTPALxg'
REFRESH_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6ImRlZmF1bHQifQ.eyJqdGkiOiJVRktFaHRveSIsImlzcyI6Imh0dHBzOi8vYWNjb3VudC5odWJzdGFmZi5jb20iLCJleHAiOjE1ODk5MjI4ODYsImlhdCI6MTU4MjE1MDQ4Niwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCBodWJzdGFmZjpyZWFkIGh1YnN0YWZmOndyaXRlIn0.fTafI8xBMth1OUraBhwq85cTaLXdfFdoomIb5zKPoA9CEuw8K6eI0aY6rcLbpLaaguzSFFudLpdMDf0cQlB7_eO1YQ7PsND-2n2MMf8xLgqrE06lGOYwjLEBlxcWvGJVS9ffnSPF8I00-Y2e_74TLBIVYdfFBF8oF2qcMy3BEsysYQgg2WgAMiHacACSeczWqmTKe0fLs6uimZuPG6EMir8Dcc3kLHRcGOMFScebJyAJzRIHqexv8xoDIP_zS4c__gBRvqqHGBmni-AFjRDOo_9lcejURzDimW2sZRDW7gZJtxOuBMJS-tzWkoKlnPdo8glSwpoR_0nugyfi8wMq4Q'
TOKEN_URL = 'https://account.hubstaff.com/access_tokens'


def get_access_token():
    token_url = 'https://account.hubstaff.com/access_tokens'

    payload = {
        'refresh_token': REFRESH_TOKEN,
        'grant_type':'refresh_token',
    }
    r = requests.post(token_url, data=payload)
    data = r.json()
    
    return data

def check_if_access_token_exists():
    if request.session.get('access_token'):
        pass
    else:
        get_access_token()


def save_task(header, project_id, task):
    url = 'https://api.hubstaff.com/v2/projects/' + project_id + '/tasks'

    r = requests.post(url, headers=header, json=task)
    print(r)
    return r

def get_task(header, task_id):
    url = 'https://api.hubstaff.com/v2/tasks/' + task_id

    r = requests.get(url, headers=header)
    data = r.json()
    data = data['task']

    data['updated_at'] = arrow.get(data['updated_at']).datetime
    data['created_at'] = arrow.get(data['created_at']).datetime

    return data

def get_tasks_for_project(header, project_id):
    url = 'https://api.hubstaff.com/v2/projects/' + project_id + '/tasks'

    r = requests.get(url, headers=header)
    data = r.json()
    data = data['tasks']

    return data

def get_projects(header):

    url = BASE_URL + 'organizations/' + ORG_ID + '/projects'

    r = requests.get(url, headers=header)
    data = r.json()
    data = data['projects']

    return data

def get_org(header):

    url = 'https://api.hubstaff.com/v2/organizations'

    r = requests.get(url, headers=header)
    data = r.json()

    return data


def token_saver(token):
    try:
        token = request.session['token']
    except:
        request.session['token'] = token


