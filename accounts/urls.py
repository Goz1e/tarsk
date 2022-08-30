"""_todo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

app_name = 'accounts'

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path('settings/', views.settings, name="settings"),
    path('delete-account/', views.delete_account, name="delete-account"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("images/favicon.ico"))),

    ]
    