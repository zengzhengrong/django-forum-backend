from rest_framework import permissions


class IsPostAuthorOrReadOnly(permissions.BasePermission):
    """只有post的author才有权限资格进行删改更新"""
    
    def has_object_permission(self, request, view, obj):
    	# SAFE_METHODS = ('GET','HEAD','OPTIONS') 也就是说这几个请求不需要通过这个类的额外许可
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.author == request.user