from django.contrib.auth.models import User, Group
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from rest_framework.generics import (
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    ListAPIView, ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    DestroyAPIView,
)
from rest_framework.response import Response
from rest_framework import status

from littlelemon.models import (
    MenuItem,
    Category,
    OrderItem,
    Cart,
    Order,
    Purchase,
    PurchaseItem,
)

from .permission import (
    IsSystemAdministrotor,
    IsManager,
    IsDeliveryCrew,
    IsCustomer,
)

from .serializers import (
    GroupSerializer,
    UserSerializer,
    MenuItemSerializer,
    CategorySerializer,
    CartSerializer,
    OrderSerializer,
    OrderItemSerializer,
    PurchaseSerializer,
    PurchaseItemSerializer,
)

from .mixins import (
    RetrieveUpdateDestroyAPIViewMixin,
    GroupManagerMixin,
    UserIsRequestedUserMixin,
    CustomerCanSeeMixin,
    CartViewHelperMixin,
    OrderListHelperMixin,
    OrderItemHelperMixin,
    OrderItemHelperMixin,
)


class UserListView(ListAPIView):
    model = User
    queryset = model.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsManager]

    def get(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='SysAdmin'):
            self.queryset = self.queryset.exclude(groups__name='SysAdmin')
        return super().get(request, *args, **kwargs)


class UserDetailView(UserIsRequestedUserMixin, RetrieveUpdateDestroyAPIView):
    model = User
    queryset = model.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsCustomer]

    def check_permissions(self, request):
        if self.user_is_requested_user(request):
            self.permission_classes = [IsCustomer]
        else:
            self.permission_classes = [IsManager]
        return super().check_permissions(request)


class GroupListViewSet(ListCreateAPIView):
    model = Group
    queryset = model.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsManager]

    def get(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='SysAdmin'):
            self.queryset = self.queryset.exclude(name='SysAdmin')
        return super().list(request, *args, **kwargs)


class GroupDetailView(ModelViewSet):
    model = Group
    queryset = model.objects.all()
    serializer_class = GroupSerializer

    def check_permissions(self, request):
        requested_group = Group.objects.get(pk=request.data.get('pk'))
        if request.method in ['GET']:
            if requested_group.name in ['SysAdmin']:
                self.permission_classes = [IsSystemAdministrotor]
            else: self.permission_classes = [IsManager]
        else:
            if requested_group.name not in ['SysAdmin', 'Manager']:
                self.permission_classes = [IsManager]
            else: self.permission_classes = [IsSystemAdministrotor]
        return super().check_permissions(request)


class SysAdminListViewSet(ModelViewSet):
    model = User
    queryset = model.objects.filter(groups__name='SysAdmin')
    serializer_class = UserSerializer
    permission_classes = [IsSystemAdministrotor]


class SysAdminDetailViewSet(SysAdminListViewSet):
    pass


class ManagerListViewSet(GroupManagerMixin, ListAPIView):
    model = User
    queryset = User.objects.filter(groups__name='Manager').exclude(groups__name='SysAdmin')
    serializer_class = UserSerializer
    group_name = 'Manager'

    def check_permissions(self, request):
        if request.method in ['POST', 'GET']:
            self.permission_classes = [IsManager]
        else:
            self.permission_classes = [IsSystemAdministrotor]
        return super().check_permissions(request)


class ManagerDetailViewSet(UserIsRequestedUserMixin, ModelViewSet):
    model = User
    queryset = User.objects.filter(groups__name='Manager').exclude(groups__name='SysAdmin')
    serializer_class = UserSerializer

    def check_permissions(self, request):
        if request.method in ['GET', 'PATCH', 'PUT', 'DELETE']:
            if self.user_is_requested_user(request):
                self.permission_classes = [IsManager]
            else: self.permission_classes = [IsSystemAdministrotor]
        else:
            self.permission_classes = [IsSystemAdministrotor]
        return super().check_permissions(request)


class DeliveryCrewListViewSet(GroupManagerMixin, ListAPIView):
    model = User
    queryset = User.objects.filter(groups__name='Delivery Crew').exclude(groups__name='SysAdmin').exclude(groups__name='Manager')
    serializer_class = UserSerializer
    permission_classes = [IsManager]
    group_name = 'Delivery Crew'
    

class DeliveryCrewDetailViewSet(UserIsRequestedUserMixin, ModelViewSet):
    model = User
    queryset = User.objects.filter(groups__name='Delivery Crew').exclude(groups__name='SysAdmin').exclude(groups__name='Manager')
    serializer_class = UserSerializer

    def check_permissions(self, request):
        if self.user_is_requested_user(request):
            self.permission_classes = [IsDeliveryCrew]
        else:
            self.permission_classes = [IsManager]
        return super().check_permissions(request)


class CustomerListViewSet(ModelViewSet):
    model = User
    queryset = User.objects.filter(groups__name='Customer').exclude(groups__name='SysAdmin').exclude(groups__name='Manager')
    serializer_class = UserSerializer

    def check_permissions(self, request):
        if request.method in ['POST']:
            self.permission_classes = []
        else:
            self.permission_classes = [IsManager]
        return super().check_permissions(request)


class CustomerDetailViewSet(UserIsRequestedUserMixin, ModelViewSet):
    model = User
    queryset = User.objects.filter(groups__name='Customer').exclude(groups__name='SysAdmin').exclude(groups__name='Manager')
    serializer_class = UserSerializer

    def check_permissions(self, request):
        if self.user_is_requested_user(request):
            self.permission_classes = [IsCustomer]
        else:
            self.permission_classes = [IsManager]
        return super().check_permissions(request)


class CategoryListViewSet(CustomerCanSeeMixin, ModelViewSet):
    model = Category
    queryset = model.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailViewSet(CustomerCanSeeMixin, ModelViewSet):
    model = Category
    queryset = model.objects.all()
    serializer_class = CategorySerializer


class MenuItemListViewSet(CustomerCanSeeMixin, ModelViewSet):
    model = MenuItem
    queryset = model.objects.all()
    serializer_class = MenuItemSerializer


class MenuItemDetailViewSet(CustomerCanSeeMixin, ModelViewSet):
    model = MenuItem
    queryset = model.objects.all()
    serializer_class = MenuItemSerializer


class CartView(CartViewHelperMixin, APIView):
    model = Cart
    queryset = model.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsCustomer]
    related_model = OrderItem

    # def check_permissions(self, request):
    #     self.permission_classes = [IsManager]
    #     if request.user.groups.exclude(name='Manager').filter(name='Customer'):
    #         if request.user == self.get_requested_user(**request.parser_context['kwargs']):
    #             self.permission_classes = [IsCustomer]
    #     return super().check_permissions(request)

    def get(self, request, *args, **kwargs):
        # user = self.get_requested_user(**kwargs)
        user = request.user
        if user:
            cart_object = self.get_or_create_cart_object(user)
            return self.object_serialized_response(request, cart_object) 
        else:
            return Response({'message': 'only customers are allowed to own a cart'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            order_item = OrderItem.objects.filter(user=user).get(pk=request.data.get('id'))
            self.add_order_item_to_cart(order_item, user)
            return Response({}, status=status.HTTP_200_OK)
        except OrderItem.DoesNotExist:
            return Response({'message': 'object does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        user = request.user
        order_item_id = request.data.get('id')
        try:
            if order_item_id is None:
                self.clear_orderitems(request, user)
            else:
                order_item = OrderItem.objects.filter(user=user).get(pk=order_item_id)
                user_cart = self.get_or_create_cart_object(user)
                user_cart.orderitems.remove(order_item)
            return Response({}, status=status.HTTP_200_OK)
        except ValueError:
            return Response({'id': 'a valid integer is required'}, status=status.HTTP_400_BAD_REQUEST)
        except OrderItem.DoesNotExist:
            return Response({'message': 'object does not exist'}, status=status.HTTP_404_NOT_FOUND)


class OrderItemListView(OrderItemHelperMixin, ListCreateAPIView):
    model = OrderItem
    related_model = MenuItem
    queryset = model.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsCustomer]

    # def check_permissions(self, request):
    #     self.permission_classes = [IsManager]
    #     if request.user.groups.exclude(name='Manager').filter(name='Customer'):
    #         if request.user == self.get_requested_user(**request.parser_context['kwargs']):
    #             self.permission_classes = [IsCustomer]
    #     return super().check_permissions(request)

    def get(self, request, *args, **kwargs):
        # user = self.get_requested_user(**kwargs)
        user = request.user
        self.queryset = self.queryset.filter(user=user)
        return super().get(request, *args, **kwargs)
    
    def post(self, request, **kwargs):
        user = request.user
        data = self.data_dict_constructor(request, user, **kwargs)
        if data is None:
            return Response({'message': 'object not found'}, status=status.HTTP_404_NOT_FOUND)
        order_item_obj = self.create_order_item_obj(data)
        return Response(status=status.HTTP_201_CREATED)
 

class OrderItemDetailView(OrderItemHelperMixin, APIView):
    model = OrderItem
    queryset = model.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsCustomer]

    # def check_permissions(self, request):
    #     self.permission_classes = [IsManager]
    #     if request.user.groups.exclude(name='Manager').filter(name='Customer'):
    #         if request.user == self.get_requested_user(**request.parser_context['kwargs']):
    #             self.permission_classes = [IsCustomer]
    #     return super().check_permissions(request)

    def get(self, request, *args, **kwargs):
        try:
            # user = self.get_requested_user(**kwargs)
            user = request.user
            order_item_obj = self.queryset.filter(user=user).get(pk=kwargs['pk'])
            serialized_object = self.serializer_class(order_item_obj)
            return Response(serialized_object.data, status=status.HTTP_200_OK)
        except self.model.DoesNotExist:
            return Response({'message': 'object not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, *args, **kwargs):
        try:
            # user = self.get_requested_user(**kwargs)
            user = request.user
            if request.data.get('quantity') is not None:
                order_item_obj = OrderItem.objects.filter(user=user).get(pk=kwargs['pk'])
                order_item_obj.quantity = int(request.data.get('quantity'))
                order_item_obj.price = order_item_obj.quantity * order_item_obj.menuitem.price
                order_item_obj.save()
                return self.object_serialized_response(request, order_item_obj)
            raise ValueError
        except ValueError:
            return Response({'quantity': 'field requires a valid integer'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': 'object not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, *args, **kwargs):
        try:
            # user = self.get_requested_user(**kwargs)
            user = request.user
            order_item_obj = OrderItem.objects.filter(user=user).get(pk=kwargs['pk'])
            order_item_obj.delete()
            return Response({}, status=status.HTTP_200_OK)
        except OrderItem.DoesNotExist:
            return Response({'message': 'object not found'})


class OrderListView(OrderListHelperMixin, ListCreateAPIView):
    model = Order
    queryset = model.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsCustomer]

    def get(self, request, *args, **kwargs):
        user = request.user
        self.queryset = self.queryset.filter(user=user)
        return super().get(request, *args, **kwargs)
    
    def post(self, request):
        user = request.user
        user_cart = self.get_user_cart(user=user)
        if user_cart is None:
            return Response({'message': 'the user does not have a cart'}, status=status.HTTP_404_NOT_FOUND)
        purchase_record = self.create_purchase_record(user, user_cart)
        self.create_order_object(user, purchase_record)
        user_cart.orderitems.clear()
        self.delete_user_order_items(user)
        user_cart.save()
        
        return Response(status=status.HTTP_201_CREATED)


class OrderDetailView(RetrieveUpdateDestroyAPIView):
    model = Order
    queryset = model.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsCustomer]


class PurchaseListView(ListAPIView):
    model = Purchase
    queryset = model.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsCustomer]

    def get(self, request, *args, **kwargs):
        user = request.user
        self.queryset = self.queryset.filter(user=user)
        return super().get(request, *args, **kwargs)


class PurchaseDetailView(RetrieveAPIView):
    model = Purchase
    queryset = model.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsCustomer]


class PurchaseItemListView(RetrieveAPIView):
    model = PurchaseItem
    queryset = model.objects.all()
    serializer_class = PurchaseItemSerializer


class PurchaseItemDetailView(PurchaseItemListView):
    pass