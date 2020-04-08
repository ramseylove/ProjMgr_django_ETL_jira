from .models import Project


def load_projects(request):
    if request.user.is_authenticated:
        user = request.user

        projects = user.projects.all()

        return {'projects': projects}
    else:
        return {}