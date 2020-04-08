# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from .services import *
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def update_projects():
    projects = get_projects()

    if projects:
        updated = update_projects_in_db(projects)
        if updated:
            update_all_issuetypes_to_db(projects)
            return 'Projects Updated Successfully'

    return 'Projects update Failed'
