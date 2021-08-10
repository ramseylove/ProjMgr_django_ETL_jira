# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger
from .services import *
from django.contrib.auth import get_user_model

User = get_user_model()

logger = get_task_logger(__name__)


@shared_task
def update_projects():
    projects = get_projects()

    if projects:
        update_projects_in_db(projects)
        update_all_issuetypes_to_db(projects)
        logger.info('Projects update successfully')

    logger.info('Projects update Failed')
    return False


@shared_task
def update_issues():

    update_all_issues_to_db()
    logger.info('issues updated successfully')
