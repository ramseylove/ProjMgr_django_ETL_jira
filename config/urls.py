from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from allauth.account.views import LoginView


urlpatterns = [
    path('notadmin/', admin.site.urls),
    path('users/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('', LoginView.as_view()),
    # path('', include('project_manager.urls')),
    # path('', include('tasks.urls')),
    path('', include('project_tracking.urls'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
] + urlpatterns
