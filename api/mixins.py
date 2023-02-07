from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User, Group

from .permission import (
    IsSystemAdministrotor,
    IsManager,
    IsDeliveryCrew,
    IsCustomer,
)

from littlelemon.models import (
    MenuItem,
    Category,
    OrderItem,
    Cart,
    Order,
    Purchase,
)


class ListCreateAPIViewMixin(ListCreateAPIView):
    related_model = None

    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(user=request.user)
        return super().get(request, *args, **kwargs)
    

class RetrieveUpdateDestroyAPIViewMixin(RetrieveUpdateDestroyAPIView):

    def get(self, request, *args, **kwargs):
        try:
            self.queryset = self.queryset.filter(user=request.user)
            return super().retrieve(request, *args, **kwargs)
        except self.model.DoesNotExist:
            return Response({'message': 'object not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, *args, **kwargs):
        try:
            self.queryset = self.queryset.filter(user=request.user)
            return super().partial_update(request, *args, **kwargs)
        except self.model.DoesNotExist:
            return Response({'message': 'object not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        try:
            self.queryset = self.queryset.filter(user=request.user)
            return super().destroy(request, *args, **kwargs)
        except self.model.DoesNotExist:
            return Response({'message': 'object not found'}, status=status.HTTP_404_NOT_FOUND)


class GroupManagerMixin:
    group_name = ''

    def post(self, request):
        try:
            user = User.objects.get(username=request.data.get('username'))
            manager_group = Group.objects.get(name=self.group_name)
            manager_group.user_set.add(user)
            manager_group.save()
            return Response(self.serializer_class(user).data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request):
        try:
            user = User.objects.get(username=request.data.get('username'))
            manager_group = Group.objects.get(name=self.group_name)
            manager_group.user_set.remove(user)
            manager_group.save()
            return Response({'message': 'user removed from the group'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)


class UserIsRequestedUserMixin:

    def user_is_requested_user(self, request):
        current_user_pk = request.user.pk
        requested_user_pk = request.parser_context['kwargs'].get('pk')
        if current_user_pk == requested_user_pk and requested_user_pk is not None:
            return True
        return False


class CustomerCanSeeMixin:

    def check_permissions(self, request):
        if not request.method in ['GET']:
            self.permission_classes = [IsManager]
        else:
            self.permission_classes = [IsCustomer]
        return super().check_permissions(request)


class CartViewHelperMixin:

    def get_model_object(self, request):
        try:
            model_object = self.queryset.get(user=request.user)
        except self.model.DoesNotExist:
            model_object = self.models.objects.create(user=request.user)
            model_object.save()
        finally:
            return model_object
    
    def get_related_object(self, request, model_object=None):
        if model_object is None:
            model_object = self.get_model_object(request) 
        try:
            id = int(request.data.get('id'))
            related_object = self.related_model.objects.filter(user=request.user).get(pk=id)
            return related_object
        except self.related_model.DoesNotExist:
            return None
    
    def serialize_object_response(self, request, model_object, status=status.HTTP_200_OK):
        serialized_data = self.serializer_class(model_object, context={'request': request})
        return Response(serialized_data.data, status=status)

    def add_or_delete(self, request, add=True):
        model_object = self.get_model_object(request)
        related_object = self.get_related_object(request, model_object)
        if related_object is None:
            return Response({'message': 'object not found'}, status=status.HTTP_404_NOT_FOUND)
        if add is True:
            model_object.orderitems.add(related_object)
            status_code = status.HTTP_201_CREATED
        else:
            model_object.orderitems.remove(related_object)
            status_code = status.HTTP_200_OK
        model_object.save()
        return self.serialize_object_response(request, model_object, status=status_code)
    
    def clear_orderitems(self, request):
        model_object = self.get_model_object(request)
        model_object.orderitems.clear()
        model_object.save()
        return self.serialize_object_response(request, model_object)


class OrderItemHelperMixin:

    def data_dict_constructor(self, request):
        try:
            related_object = self.related_model.objects.get(pk=request.data.get('id'))
            quantity = request.data.get('quantity')
            quantity = 1 if quantity is None else int(quantity)
            unit_price = related_object.price
            price = unit_price * quantity

            data = {
                'user': request.user,
                'related_object': related_object,
                'quantity': quantity,
                'unit_price': unit_price,
                'price': price,
            }
            return data
        except self.model.DoesNotExist:
            return None

    def create_object(self, data):
        model_object = self.model.objects.create(
            user = data['user'],
            menuitem = data['related_object'],
            quantity = data['quantity'],
            unit_price = data['unit_price'],
            price = data['price'],
        )
        return model_object


class OrderListHelperMixin:

    def get_user_cart(self, request):
        try:
            return Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return None
    
    def create_purchase_record(self, request, user_cart):
        purchase = Purchase.objects.create(user=request.user)
        purchase.orderitems.set(user_cart.orderitems.all())
        purchase.save()
        return purchase
    
    def get_purchase_cost(self, purchase_record):
        total_cost = 0
        for orderidem in purchase_record.orderitems.all():
            total_cost += orderidem.price
        return total_cost
    
    def create_order_object(self, request, purchase_record):
        order_object = self.model.objects.create(
            user = request.user,
            purchase = purchase_record,
            total = self.get_purchase_cost(purchase_record)
        )
        order_object.save()
        return order_object
