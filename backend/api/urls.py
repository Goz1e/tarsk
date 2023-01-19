from .views import (
    api_root,TaskList,ActiveTaskList,TaskDetail,SearchView,
    AddDependencyAndCollaborator ,RemoveDependencyAndCollaborator,
    CommentView, CommentDeleteView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path

urlpatterns = [
    path('', api_root, name='api_index'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('search/', SearchView.as_view(), name='search'),
    path('task-list', TaskList.as_view(), name='task-list'),
    path('active-task', ActiveTaskList.as_view(), name='active-tasks'),
    path('<str:slug>/', TaskDetail.as_view(), name='task-detail'),
    path('<str:slug>/add-comment/', CommentView.as_view(), name='add-comment'),
    path('comment/<int:id>/delete/', CommentDeleteView.as_view(), name='delete-comment'),
    path('<slug:slug>/add-dep/', AddDependencyAndCollaborator.as_view(), name='add_dep'),
    path('<slug:slug>/remove-dep/', RemoveDependencyAndCollaborator.as_view(), name='remove_dep'),
]