from django.contrib import admin
from django.urls import path, include
from native_auth.views import landing_page


urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include('api.urls')),
    path('account/', include('native_auth.urls')),
    path('accounts/', include('allauth.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('task/', include('task.urls')),
    path('admin/', admin.site.urls),
]