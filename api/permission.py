from rest_framework.permissions import BasePermission, IsAuthenticated


class PermissionBaseMixin(BasePermission):
    group = ''

    def has_permission(self, request, view):
        if not bool(request.user and request.user.is_authenticated):
            return False
        if not request.user.groups.filter(name=self.group):
            return False
        return True


class IsSystemAdministrotor(PermissionBaseMixin):
    group = 'SysAdmin'


class IsManager(PermissionBaseMixin):
    group = 'Manager'


class IsDeliveryCrew(PermissionBaseMixin):
    group = 'Delivery Crew'


class IsCustomer(PermissionBaseMixin):
    group = 'Customer'