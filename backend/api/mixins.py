from rest_framework import  permissions
from .permissions import MyCustomPermissions

class StaffEditorPermissionMixin():
    permission_classes = [permissions.IsAdminUser,MyCustomPermissions]
    

class UserQuerySetMixin():
    def get_queryset(self,*args,**kwargs):
        return super().get_queryset().filter(user=self.request.user)    
