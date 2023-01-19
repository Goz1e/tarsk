from django import views
from django.urls import path
from .views import *

app_name= 'task'
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('search/', search, name='search'),
    path('create/', create_task, name='create'),
    path('test/', test, name='test'),
    path('<slug:slug>/', detail, name='detail'),
    path('<slug:slug>/update/', update, name='update'),
    path('<slug:slug>/completed/', completed, name='completed'),
    path('<slug:slug>/add_comment/', add_comment, name='add_comment'),
    # path('<slug:slug>/update-dependencies/', update_dependencies, name='update_dependencies'),
    path('<slug:slug>/collaborators/', update_collab, name='update_collabs'),
    path('<slug:slug>/delete/', delete_task, name='delete'),
    path('<int:id>/delete-comment/', delete_comment, name='delete_comment'),
    path('<slug:slug>/remove-collab/<str:user_id>/<str:dashboard>/', remove_collab, name='remove_collab'),
    path('<slug:slug>/update-dep/', update_dep, name='update_dep'),
    path('<slug:slug>/remove-dep/<str:dep_id>', remove_dep, name='remove_dep'),
    
]