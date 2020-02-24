from django.conf import settings

import arrow
import json
import requests




def client():
    BASE_URL = 'https://atriadev.atlassian.net/rest/api/v3project/search'
    TOKEN = settings.JIRA_KEY
    USER = settings.JIRA_USER

    r = requests.get(BASE_URL, auth=(USER, TOKEN))
    data = j.json()

    print(r)
    return data