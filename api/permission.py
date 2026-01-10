from rest_framework.permissions import BasePermission


class IsTeacher(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, 'role', '') == 'teacher')


class IsStudent(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, 'role', '') == 'student')

class IsAdmin(BasePermission):

    def has_permission(self, request, view):
       if not request.user or not request.user.is_authenticated:
            return False
       if request.user.is_superuser:
            return True
       return getattr(request.user,'role','')=='admin'
