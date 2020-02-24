from .services import get_project

# def load_projects(request):
#     user = request.user
#     projects = []

#     for p in user.projects.all():
#         project = get_project(p.p_key)
#         projects.append(project)
#     return {'projects':projects}