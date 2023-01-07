from django.urls import path
from .views import (
    login_view, signup, edit_profile,settings,
    logout_view,delete_native_auth
)

app_name = 'native_auth'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup, name='signup'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('logout/', logout_view, name='logout'),
    path('settings/', settings, name='settings'),
    path('delete-account/', delete_native_auth, name='delete-account'),
]