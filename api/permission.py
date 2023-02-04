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


class IsCustomer(BasePermission):
    customer_allowed_methods = ['GET']
    requires_customer_authentication = True

    def has_permission(self, request, view):
        if not request.method in self.customer_allowed_methods:
            return False
        if not self.requires_customer_authentication:
            return True
        if not bool(request.user and request.user.is_authenticated):
            return False
        return True
