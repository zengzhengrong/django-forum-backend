from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """只有UserAdmin才有权限资格进行"""
    
    def has_permission(self, request, view):
    	# SAFE_METHODS = ('GET','HEAD','OPTIONS') 也就是说这几个请求不需要通过这个类的额外许可
        if request.method in permissions.SAFE_METHODS:
            if view.action in ['retrieve']:
                return request.user.is_authenticated and request.user.is_superuser
            return True
        

        # 当userprofile的id和当前认证的用户指向同一个profile时才返回True
        return request.user.is_superuser