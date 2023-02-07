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
    MenuItem, Category,
    OrderItem, Cart, Purchase, Order,
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
)

from .mixins import (
    RetrieveUpdateDestroyAPIViewMixin,
    GroupManagerMixin,
    UserIsRequestedUserMixin,
    CustomerCanSeeMixin,
    CartViewHelperMixin,
    OrderItemHelperMixin,
    OrderListHelperMixin,
)


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


class OrderItemListViewSet(OrderItemHelperMixin, RetrieveAPIView):
    model = OrderItem
    related_model = MenuItem
    queryset = model.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsCustomer]

    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(user=request.user)
        return super().get(request, *args, **kwargs)
    
    def post(self, request):
        data = self.data_dict_constructor(request)
        if data is None:
            return Response({'message': 'object not found'}, status=status.HTTP_404_NOT_FOUND)
        model_object = self.create_object(data)
        serialized_object = self.serializer_class(model_object)
        return Response(serialized_object.data, status=status.HTTP_201_CREATED)
        
    def delete(self, request):
        try:
            if not request.data.get('id') is None:
                instance = self.queryset.filter(user=request.user).get(pk=request.data.get('id'))
                instance.delete()
            else:
                self.queryset.filter(user=request.user).delete()
            return self.get(request)
        except self.model.DoesNotExist:
            return Response({'message': 'object not found'}, status=status.HTTP_404_NOT_FOUND)


class OrderItemDetailViewSet(RetrieveUpdateAPIView):
    model = OrderItem
    queryset = model.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsCustomer]

    def get(self, request, *args, **kwargs):
        try:
            query_object = self.queryset.filter(user=request.user).get(pk=kwargs['pk'])
            serialized_object = self.serializer_class(query_object)
            return Response(serialized_object.data, status=status.HTTP_200_OK)
        except self.model.DoesNotExist:
            return Response({'message': 'object not found'}, status=status.HTTP_404_NOT_FOUND)
    

class CartViewSet(CartViewHelperMixin, RetrieveUpdateDestroyAPIView):
    model = Cart
    queryset = model.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsCustomer]
    related_model = OrderItem

    def get(self, request):
        model_object = self.get_model_object(request)
        serialized_data = self.serializer_class(model_object, context={'request': request}) 
        return Response(serialized_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        return self.add_or_delete(request, add=True)

    def delete(self, request):
        if request.data.get('id') is None:
            return self.clear_orderitems(request)
        return self.add_or_delete(request, add=False)


class PurchaseListView(ListCreateAPIView):
    model = Purchase
    queryset = model.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsCustomer]

    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(user=request.user)
        return super().get(request, *args, **kwargs)


class PurchaseDetailView(RetrieveAPIView):
    model = Purchase
    queryset = model.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsCustomer]
    

class OrderListViewSet(OrderListHelperMixin, ListCreateAPIView):
    model = Order
    queryset = model.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsCustomer]

    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(user=request.user)
        return super().get(request, *args, **kwargs)
    
    def post(self, request):
        """
        Take all orderitems present in the Cart table and place them in a new Purchase instance,
        relate that Purchase instance to a new Order instance
        """
        user_cart = self.get_user_cart(request)
        purchase_record = self.create_purchase_record(request, user_cart)
        order_object = self.create_order_object(request, purchase_record)
        user_cart.orderitems.clear()
        user_cart.save()
        
        serialized_object = self.serializer_class(order_object)
        return Response(serialized_object.data, status=status.HTTP_201_CREATED)


class OrderDetailViewSet(ModelViewSet):
    model = Order
    queryset = model.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsCustomer]


class UserDetailView(APIView):
    model = User
    queryset = model.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsCustomer]

    def get(self, request, pk):
        user = self.model.objects.get(pk=request.user.pk)
        serialized_object = self.serializer_class(user)
        return Response(serialized_object.data, status=status.HTTP_200_OK)
