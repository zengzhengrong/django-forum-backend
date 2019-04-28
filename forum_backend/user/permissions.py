from rest_framework import permissions


class IsUserOwnerOrReadOnly(permissions.BasePermission):
    """只有User自己才有权限资格进行删改更新"""
    
    def has_object_permission(self, request, view, obj):
    	# SAFE_METHODS = ('GET','HEAD','OPTIONS') 也就是说这几个请求不需要通过这个类的额外许可
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 当user的id和当前认证的用户指向同一个id时才返回True
        return obj.id == request.user.id

class IsAdmin(permissions.BasePermission):
    """只有UserAdmin才有权限资格进行get a list of user"""
    
    def has_permission(self, request, view):
    	# SAFE_METHODS = ('GET','HEAD','OPTIONS') 也就是说这几个请求不需要通过这个类的额外许可
        safe_methods = list(permissions.SAFE_METHODS)
        # 删除GET 方法
        safe_methods.remove('GET')
        if request.method in safe_methods:
            return True
        
        # 当userprofile的id和当前认证的用户指向同一个profile时才返回True
        return request.user.is_superuser