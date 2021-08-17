This project management application was build to Extract, Transform, and Load Jira Project data from my businesses Jira
account. Idea was to have control over project information that clients would see, along with simplify their experience.

Flow:
When a Super User logs in to the admin panel, the service layer creates a task to request all projects and issues from the Jira api.
It is then transformed into a dataframe and uses Jira Id field to compare agains local db data to determine if there are new or deleted projects.
Then for issues it compares the Jira updated time with local db 
An admin needs to log in to create a user and link projects to the users before they can see any data. Super admins can
see all projects.

Once a user logs in, the requests made to the jira api are directly made and new / updated data is pulled into the
database. Including posting Issues to Jira and DB.

Comments were never implemented and project was abandoned.

## Built with

* Jira V2 api 
* Docker-compose 
* Postgres 11
* S3 compatible storage - I used Digital Ocean
* SendGrid - Smtp email service
* Celery 4 - Task Queue 
* RabbitMQ - Message Broker 
* Migrated to Pip to handle virtual envrionments

### Environment variables that need to be defined in env/dev.env file
```
COMPOSE_PROJECT_NAME 
SECRET_KEY 
ENVIRONMENT=docker_development # or production
DEBUG=1 
ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0

SPACES_BUCKET_NAME=  
SPACES_ACCESS_KEY_ID= 
SPACES_SECRET_ACCESS_TOKEN= 
SPACES_SECRET_ACCESS_KEY=

SENDGRID_SMTPKEY= 
JIRA_KEY=

DB_USER= 
DB_PORT= 
DB_HOST=
```

## Base Project

The base Project was built using [DjangoX](https://github.com/wsvincent/djangox) template created by Will vincent

### Base Features

- For Django 2.2 and Python 3.7
- Modern virtual environments with [pipenv](https://github.com/pypa/pipenv)
- Styling with [Bootstrap](https://github.com/twbs/bootstrap) v4.1.3
- Custom user model
- Email/password for log in/sign up instead of Django's default username/email/password pattern
- Social authentication via [django-allauth](https://github.com/pennersr/django-allauth)
- [django-debug-toolbar](https://github.com/jazzband/django-debug-toolbar)

## Other resources

- Use [PostgreSQL locally via Docker](https://wsvincent.com/django-docker-postgresql/)
- Use [django-environ](https://github.com/joke2k/django-environ) for environment variables
- Update [EMAIL_BACKEND](https://docs.djangoproject.com/en/2.0/topics/email/#module-django.core.mail) to configure an
  SMTP backend
- Make the [admin more secure](https://opensource.com/article/18/1/10-tips-making-django-admin-more-secure)
