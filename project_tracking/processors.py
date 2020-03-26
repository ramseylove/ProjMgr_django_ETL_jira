from .models import Project


def load_projects(request):
    user = request.user

    projects = user.projects.all()

    return { 'projects': projects }
