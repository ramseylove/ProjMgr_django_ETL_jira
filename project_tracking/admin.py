from django.contrib import admin
from django.urls import path


from .models import Project, Issue, IssueTypes


class ProjectAdmin(admin.ModelAdmin):
    change_list_template = "users/project_change_list.html"
    list_display=(
        'key',
        'name',
        'category_name'
    )
    ordering = ('category_name',)
    readonly_fields = [
        'id',
        'key',
        'name',
        'category_id',
        'category_name',
        'description',
    ]
    
    # def get_urls(self):
    #     urls = super().get_urls()
    #     my_urls = [
    #         path('load_issues/',  name='load_issues'),
    #         path('load_issue_types/', load_issue_types_view, name='load_issue_types'),
    #         path('load_projects/', load_projects_view, name='load_projects'),
    #     ]
    #     return my_urls + urls

    # def update_projects(self, request):
    #     projects = save_projects()
    #     self.message_user(request, "Projects have been updated")
    #     return HttpResponseRedirect("../")

class IssueAdmin(admin.ModelAdmin):
    list_display=(
        'key',
        'summary',
        'issue_type'
    )
    readonly_fields = [
        'id',
        'key',
        'url',
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
class IssueTypesAdmin(admin.ModelAdmin):
    list_display=(
        'id',
        'name',
        'project',

    )

admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(IssueTypes, IssueTypesAdmin)
