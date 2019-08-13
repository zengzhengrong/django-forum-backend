from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """只有UserAdmin才有权限资格进行"""
    
    def has_permission(self, request, view):
    	# SAFE_METHODS = ('GET','HEAD','OPTIONS') 也就是说这几个请求不需要通过这个类的额外许可
        # 当action是retrieve则要管理员权限
        if request.method in permissions.SAFE_METHODS:
            if view.action in ['retrieve']:
                return request.user.is_authenticated and request.user.is_superuser
            return True
        

        # 其余都要管理员权限
        return request.user.is_superuser

class IsCommentAuthorOrReadOnly(permissions.BasePermission):
    """只有Comment的author才有权限资格进行删改更新"""
    
    def has_object_permission(self, request, view, obj):
    	# SAFE_METHODS = ('GET','HEAD','OPTIONS') 也就是说这几个请求不需要通过这个类的额外许可
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.user == request.user