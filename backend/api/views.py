from rest_framework import permissions,authentication
from task.models import Task,Comment
from .serializers import TaskSerializer, TaskDetailSerializer, CommentSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import status, mixins, generics
from rest_framework.generics  import UpdateAPIView, ListAPIView, GenericAPIView
from django.shortcuts import get_object_or_404
from .permissions import IsOwnerOrReadOnly
# Create your views here.


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'user tasks': reverse('task-list', request=request, format=format),
        'active tasks': reverse('active-tasks', request=request, format=format),
    })

class TaskList(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ActiveTaskList(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.active_tasks(user=self.request.user)  

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    lookup_field = 'slug'

class AddDependencyAndCollaborator(UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = "slug"
    
    def patch(self,request,*args,**kwargs):
        task = self.get_object()
        if 'dep_list' in request.data:
            dep_list = self.request.data.pop('dep_list')
            for dep in dep_list:
                task.dependencies.add(dep)
        if 'collab_list' in request.data:
            collab_list = self.request.data.pop('collab_list')
            for collab in collab_list:
                task.collaborators.add(collab)
        task.save()
        serializer = TaskSerializer(task,context={'request': request})
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    
class RemoveDependencyAndCollaborator(UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = "slug"
        
    def patch(self,request,*args,**kwargs):
        task = self.get_object()
        if 'dep_list' in request.data:
            dep_list = self.request.data.pop('dep_list')
            for dep in dep_list:
                task.dependencies.remove(dep)
        if 'collab_list' in request.data:
            collab_list = self.request.data.pop('collab_list')
            for collab in collab_list:
                task.collaborators.remove(collab)
        task.save()
        serializer = TaskSerializer(task,context={'request': request})
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

class SearchView(ListAPIView):
    serializer_class = TaskSerializer
    authentication_classes= [authentication.SessionAuthentication,]
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'id'

    def get_queryset(self,*args,**kwargs):
        qs = super().get_queryset(*args,**kwargs)
        q = self.request.GET.get("q")
        result = Task.objects.none()
        
        if q is not None:
            user = self.request.user
            result = qs.search(user,q)
        return result

class CommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = []
    lookup_field = 'id'

    def perform_create(self, serializer):
        print(self.request.data)
        serializer.save(author = self.request.user)

class CommentDeleteView(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    lookup_field = 'id'
