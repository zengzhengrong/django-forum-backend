from rest_framework import permissions


class IsAdminDelete(permissions.BasePermission):
    """只有UserAdmin才有权限资格进行destroy"""
    
    def has_permission(self, request, view):
    	# SAFE_METHODS = ('GET','HEAD','OPTIONS') 也就是说这几个请求不需要通过这个类的额外许可
        # 当action是retrieve则要管理员权限
        # 'retrieve', 'destroy' 需要管理员权限
        # 
        if request.method in permissions.SAFE_METHODS:
            if view.action in ['retrieve']:
                return request.user.is_authenticated and request.user.is_superuser
            
            return True
        if request.method == 'DELETE' and view.action == 'destroy':
            return request.user.is_authenticated and request.user.is_superuser

        # 其余都要登陆
        return bool(request.user and request.user.is_authenticated)

class IsCommentAuthorOrReadOnly(permissions.BasePermission):
    """只有Comment的author才有权限资格进行删改更新"""
    
    def has_object_permission(self, request, view, obj):
    	# SAFE_METHODS = ('GET','HEAD','OPTIONS') 也就是说这几个请求不需要通过这个类的额外许可
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.user == request.user