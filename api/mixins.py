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
    Category,
    MenuItem,
    OrderItem,
    Cart,
    Order,
    PurchaseItem,
    Purchase,
)


class UserHelperMixin:

    def user_is_requested_user(self, request):
        user_pk = request.user.pk
        requested_user_pk = request.parser_context['kwargs'].get('pk')
        if user_pk == requested_user_pk and requested_user_pk is not None:
            return True
        return False

    def user_in_group(self, request, group_name=''):
        user = request.user
        if user.groups.filter(name=group_name):
            return True
        return False

    def requested_user_in_group(self, request, group_name=''):
        user_pk = request.parser_context['kwargs'].get('pk')
        user = User.objects.get(pk=user_pk)
        if user.groups.filter(name=group_name):
            return True
        return False
    
    def user_is_unathentictaed(self, request):
        return request.user.is_anonymous

    def user_is_customer(self, request):
        return self.user_in_group(request, group_name='Customer')

    def user_is_delivery_crew(self, request):
        return self.user_in_group(request, group_name='Delivery Crew')

    def user_is_manager(self, request):
        return self.user_in_group(request, group_name='Manager')

    def user_is_admin(self, request):
        return self.user_in_group(request, group_name='SysAdmin')

    def requested_user_is_customer(self, request):
        return self.requested_user_in_group(request, group_name='Customer')

    def requested_user_is_delivery_crew(self, request):
        return self.requested_user_in_group(request, group_name='Delivery Crew')

    def requested_user_is_manager(self, request):
        return self.requested_user_in_group(request, group_name='Manager')

    def requested_user_is_admin(self, request):
        return self.requested_user_in_group(request, group_name='SysAdmin')


class CommonUtilsMixin:

    def object_serialized_response(self, request, object, status=status.HTTP_200_OK):
        serialized_data = self.serializer_class(object, context={'request': request})
        return Response(serialized_data.data, status=status)

    def get_requested_user(self, **kwargs):
        user_queryset = User.objects.filter(groups__name='Customer').exclude(groups__name='Manager')
        try:
            return user_queryset.get(pk=kwargs['pk'])
        except User.DoesNotExist:
            return None


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


class GroupListHelperMixin:
    group_name = ''

    def post(self, request):
        try:
            user_id = int(request.data.get('id'))
            user = User.objects.get(pk=user_id)
            group = Group.objects.get(name=self.group_name)
            group.user_set.add(user)
            group.save()
            return Response(self.serializer_class(user).data, status=status.HTTP_201_CREATED)
        except ValueError:
            return Response({'id': 'a valid integer is required'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': 'object not found'}, status=status.HTTP_404_NOT_FOUND)
        

class GroupDetailHelperMixin:

    def delete(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=kwargs['pk'])
            group = Group.objects.get(name=self.group_name)
            group.user_set.remove(user)
            group.save()
            return Response({'message': 'user removed from the group'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'object not found'}, status=status.HTTP_404_NOT_FOUND)


class CustomerCanSeeMixin:

    def check_permissions(self, request):
        if not request.method in ['GET']:
            self.permission_classes = [IsManager]
        else:
            self.permission_classes = [IsCustomer]
        return super().check_permissions(request)


class CartViewHelperMixin(CommonUtilsMixin):

    def get_or_create_cart_object(self, user):
        try:
            return self.model.objects.get(user=user)
        except self.model.DoesNotExist:
            cart_object = self.model.objects.create(user=user)
            cart_object.save()
            return cart_object

    def create_order_item_obj(self, request, user, menu_item_obj):
        quantity = request.data.get('quantity')
        quantity = 1 if quantity is None else int(quantity)
        unit_price = menu_item_obj.price
        price = unit_price * quantity

        order_item_obj = OrderItem.objects.create(
            user = user,
            menuitem = menu_item_obj,
            quantity = quantity,
            unit_price = unit_price,
            price = price, 
        )
        return order_item_obj

    def get_order_item(self, request, user):
        try:
            id = int(request.data.get('id'))
            order_item = OrderItem.objects.filter(user=user).get(pk=id)
            return order_item
        except OrderItem.DoesNotExist:
            return None

    def add_order_item_to_cart(self, order_item_obj, user):
        cart_object = self.get_or_create_cart_object(user)
        cart_object.orderitems.add(order_item_obj)
        cart_object.save()
    
    def delete_order_item_from_cart(self, order_item_obj, user):
        cart_object = self.get_or_create_cart_object(user)
        cart_object.orderitems.remove(order_item_obj)
        cart_object.save()
    
    def clear_orderitems(self, request, user):
        cart_object = self.get_or_create_cart_object(user)
        cart_object.orderitems.clear()
        cart_object.save()


class OrderItemHelperMixin(CommonUtilsMixin):

    def data_dict_constructor(self, request, user, **kwargs):
        try:
            menu_item_obj = MenuItem.objects.get(pk=request.data.get('id'))
            quantity = request.data.get('quantity')
            quantity = 1 if quantity is None else int(quantity)
            unit_price = menu_item_obj.price
            price = unit_price * quantity

            data = {
                'user': user,
                'related_object': menu_item_obj,
                'quantity': quantity,
                'unit_price': unit_price,
                'price': price,
            }
            return data
        except MenuItem.DoesNotExist:
            return None

    def create_order_item_obj(self, data):
        order_item_obj = OrderItem.objects.create(
            user = data['user'],
            menuitem = data['related_object'],
            quantity = data['quantity'],
            unit_price = data['unit_price'],
            price = data['price'],
        )
        return order_item_obj


class OrderListHelperMixin(CommonUtilsMixin):

    def get_user_cart(self, user):
        try:
            return Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return None
    
    def create_purchase_item_from_order_item(self, order_item):
        purchase_item = PurchaseItem.objects.create(
            user = order_item.user,
            menuitem = order_item.menuitem,
            quantity = order_item.quantity,
            unit_price = order_item.unit_price,
            price = order_item.price,
        )
        purchase_item.save()
        return purchase_item
    
    def create_purchase_record(self, user, user_cart):
        purchase = Purchase.objects.create(user=user)
        for order_item in user_cart.orderitems.all():
            purchase_item = self.create_purchase_item_from_order_item(order_item)
            purchase.purchaseitems.add(purchase_item)
        purchase.save()
        return purchase
    
    def get_purchase_cost(self, purchase_record):
        total_cost = 0
        for purchase_item in purchase_record.purchaseitems.all():
            total_cost += purchase_item.price
        return total_cost
    
    def create_order_object(self, user, purchase_record):
        order_object = self.model.objects.create(
            user = user,
            purchase = purchase_record,
            total = self.get_purchase_cost(purchase_record)
        )
        order_object.save()
        return order_object
    
    def delete_user_order_items(self, user):
        order_items = OrderItem.objects.filter(user=user).delete()
        if OrderItem.objects.filter(user=user).all():
            return False
        return True


class PurchaseDetailHelperMixin(CommonUtilsMixin):
    pass
