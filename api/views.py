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
    IsCustomerOrDeliveryCrew,
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
    GroupListHelperMixin,
    GroupDetailHelperMixin,
    UserHelperMixin,
    CustomerCanSeeMixin,
    CartViewHelperMixin,
    OrderListHelperMixin,
    OrderItemHelperMixin,
    OrderItemHelperMixin,
    PurchaseDetailHelperMixin,
    CommonUtilsMixin,
)


class UserListView(UserHelperMixin, ListCreateAPIView):
    model = User
    queryset = model.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsManager]
    ordering_fields = ['username', 'first_name', 'last_name']
    search_fields = ['username', 'first_name', 'last_name']
    filterset_fields = ['username', 'first_name', 'last_name']

    def check_permissions(self, request):
        self.permission_classes = [IsManager]
        if request.method == 'POST' and self.user_is_unathentictaed(request):
            self.permission_classes = []
        return super().check_permissions(request)

    def get(self, request, *args, **kwargs):
        if not self.user_is_admin(request):
            self.queryset = self.queryset.exclude(groups__name='SysAdmin')
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        serialized_data = self.serializer_class(data=request.data)
        serialized_data.is_valid(raise_exception=True)
        self.perform_create(serialized_data)
        return Response(serialized_data.data, status=status.HTTP_201_CREATED)


class UserDetailView(UserHelperMixin, RetrieveUpdateDestroyAPIView):
    model = User
    queryset = model.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsCustomerOrDeliveryCrew]

    def check_permissions(self, request):
        self.permission_classes = [IsSystemAdministrotor]
        if self.user_is_requested_user(request):
            self.permission_classes = {IsCustomerOrDeliveryCrew}
        elif self.user_is_admin(request):
            pass
        elif self.requested_user_is_admin(request):
            pass
        elif self.user_is_manager(request):
            if self.requested_user_is_manager(request):
                if request.method in ['GET']:
                    self.permission_classes = [IsManager]
            else:
                self.permission_classes = [IsManager]
        return super().check_permissions(request)
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


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
        pk = request.parser_context['kwargs']['pk']
        requested_group = Group.objects.get(pk=pk)
        if request.method in ['GET']:
            if requested_group.name in ['SysAdmin']:
                self.permission_classes = [IsSystemAdministrotor]
            else: self.permission_classes = [IsManager]
        else:
            if requested_group.name not in ['SysAdmin', 'Manager']:
                self.permission_classes = [IsManager]
            else: self.permission_classes = [IsSystemAdministrotor]
        return super().check_permissions(request)
    
    def get(self, request, *args, **kwargs):
        group = Group.objects.get(pk=kwargs['pk'])
        serialized_data = self.serializer_class(group)
        return Response(serialized_data.data, status=status.HTTP_200_OK)


class SysAdminListView(GroupListHelperMixin, ListAPIView):
    model = User
    queryset = model.objects.filter(groups__name='SysAdmin')
    serializer_class = UserSerializer
    permission_classes = [IsSystemAdministrotor]
    group_name = 'SysAdmin'
    ordering_fields = ['username', 'first_name', 'last_name']
    search_fields = ['username', 'first_name', 'last_name']
    filterset_fields = ['username', 'first_name', 'last_name']


class SysAdminDetailViewSet(GroupDetailHelperMixin, RetrieveUpdateAPIView):
    model = User
    queryset = model.objects.filter(groups__name='SysAdmin')
    serializer_class = UserSerializer
    permission_classes = [IsSystemAdministrotor]
    group_name = 'SysAdmin'


class ManagerListView(GroupListHelperMixin, ListAPIView):
    model = User
    queryset = User.objects.filter(groups__name='Manager').exclude(groups__name='SysAdmin')
    serializer_class = UserSerializer
    group_name = 'Manager'
    ordering_fields = ['username', 'first_name', 'last_name']
    search_fields = ['username', 'first_name', 'last_name']
    filterset_fields = ['username', 'first_name', 'last_name']

    def check_permissions(self, request):
        if request.method in ['POST', 'GET']:
            self.permission_classes = [IsManager]
        else:
            self.permission_classes = [IsSystemAdministrotor]
        return super().check_permissions(request)


class ManagerDetailView(UserHelperMixin, GroupDetailHelperMixin, RetrieveUpdateAPIView):
    model = User
    queryset = User.objects.filter(groups__name='Manager').exclude(groups__name='SysAdmin')
    serializer_class = UserSerializer
    group_name = 'Manager'

    def check_permissions(self, request):
        if self.user_is_requested_user(request):
            self.permission_classes = [IsManager]
        elif request.method in ['GET']:
            self.permission_classes = [IsManager]
        else: self.permission_classes = [IsSystemAdministrotor]
        return super().check_permissions(request)


class DeliveryCrewListView(GroupListHelperMixin, ListAPIView):
    model = User
    queryset = User.objects.filter(groups__name='Delivery Crew').exclude(groups__name='SysAdmin').exclude(groups__name='Manager')
    serializer_class = UserSerializer
    permission_classes = [IsManager]
    group_name = 'Delivery Crew'
    ordering_fields = ['username', 'first_name', 'last_name']
    search_fields = ['username', 'first_name', 'last_name']
    filterset_fields = ['username', 'first_name', 'last_name']
    

class DeliveryCrewDetailView(GroupDetailHelperMixin, RetrieveUpdateAPIView):
    model = User
    queryset = User.objects.filter(groups__name='Delivery Crew').exclude(groups__name='SysAdmin').exclude(groups__name='Manager')
    serializer_class = UserSerializer
    permission_classes = [IsManager]
    group_name = 'Delivery Crew'


class CustomerListView(GroupListHelperMixin, ListAPIView):
    model = User
    queryset = User.objects.filter(groups__name='Customer').exclude(groups__name='SysAdmin').exclude(groups__name='Manager')
    serializer_class = UserSerializer
    permission_classes = [IsManager]
    group_name = 'Customer'
    ordering_fields = ['username', 'first_name', 'last_name']
    search_fields = ['username', 'first_name', 'last_name']
    filterset_fields = ['username', 'first_name', 'last_name']


class CustomerDetailView(GroupDetailHelperMixin, RetrieveUpdateAPIView):
    model = User
    queryset = User.objects.filter(groups__name='Customer').exclude(groups__name='SysAdmin').exclude(groups__name='Manager')
    serializer_class = UserSerializer
    permission_classes = [IsManager]
    group_name = 'Customer'


class CategoryListView(ModelViewSet):
    model = Category
    queryset = model.objects.all()
    serializer_class = CategorySerializer
    ordering_fields = ['title', 'slug']
    search_fields = ['title', 'slug']
    filterset_fields = ['title', 'slug']

    def check_permissions(self, request):
        if request.method in ['GET']:
            self.permission_classes = [IsCustomerOrDeliveryCrew]
        else:
            self.permission_classes = [IsManager]
        return super().check_permissions(request)


class CategoryDetailView(ModelViewSet):
    model = Category
    queryset = model.objects.all()
    serializer_class = CategorySerializer

    def check_permissions(self, request):
        if request.method in ['GET']:
            self.permission_classes = [IsCustomerOrDeliveryCrew]
        else:
            self.permission_classes = [IsManager]
        return super().check_permissions(request)


class CategoryMenuItemsView(ListAPIView):
    model = MenuItem
    queryset = model.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['title', 'price', 'featured']
    search_fields = ['title', 'price', 'featured']
    filterset_fields = ['title', 'price', 'featured']

    def check_permissions(self, request):
        if request.method in ['GET']:
            self.permission_classes = [IsCustomerOrDeliveryCrew]
        else:
            self.permission_classes = [IsManager]
        return super().check_permissions(request)
    
    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(category__pk=kwargs['pk'])
        return super().get(request, *args, **kwargs)
    

class MenuItemListView(ModelViewSet):
    model = MenuItem
    queryset = model.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['title', 'price', 'featured']
    search_fields = ['title', 'price', 'featured']
    filterset_fields = ['title', 'price', 'featured']

    def check_permissions(self, request):
        if request.method in ['GET']:
            self.permission_classes = [IsCustomerOrDeliveryCrew]
        else:
            self.permission_classes = [IsManager]
        return super().check_permissions(request)
    
    def get_queryset(self):
        query_param_value = self.request.query_params.get('category')
        if query_param_value is not None:
            try:
                category = Category.objects.get(pk=int(query_param_value))
            except ValueError:
                category = Category.objects.get(title=query_param_value)
            self.queryset = self.queryset.filter(category=category)
        return super().get_queryset()


class MenuItemDetailView(ModelViewSet):
    model = MenuItem
    queryset = model.objects.all()
    serializer_class = MenuItemSerializer

    def check_permissions(self, request):
        if request.method in ['GET']:
            self.permission_classes = [IsCustomerOrDeliveryCrew]
        else:
            self.permission_classes = [IsManager]
        return super().check_permissions(request)


class CartView(CartViewHelperMixin, APIView):
    model = Cart
    queryset = model.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsCustomer]
    related_model = OrderItem

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.groups.filter(name='Customer') and len(user.groups) == 1:
            return Response({'message': 'Only Customers are allowed to own a Cart'}, status=status.HTTP_400_BAD_REQUEST)
        cart_object = self.get_or_create_cart_object(user)
        return self.object_serialized_response(request, cart_object) 

    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.groups.filter(name='Customer') and len(user.groups) == 1:
            return Response({'message': 'Only Customers are allowed to own a Cart'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            order_item = OrderItem.objects.filter(user=user).get(pk=request.data.get('id'))
            self.add_order_item_to_cart(order_item, user)
            return Response({}, status=status.HTTP_200_OK)
        except OrderItem.DoesNotExist:
            return Response({'message': 'object does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        user = request.user
        if not user.groups.filter(name='Customer') and len(user.groups) == 1:
            return Response({'message': 'Only Customers are allowed to own a Cart'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            order_item_id = request.data.get('id')
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
    ordering_fields = ['user', 'menuitem']
    search_fields = ['user', 'menuitem']
    filterset_fields = ['user', 'menuitem']

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.groups.filter(name='Manager'):
            self.queryset = self.queryset.filter(user=user)
        return super().get(request, *args, **kwargs)
    
    def post(self, request, **kwargs):
        user = request.user
        data = self.data_dict_constructor(request, user, **kwargs)
        if data is None:
            return Response({'message': 'object not found'}, status=status.HTTP_404_NOT_FOUND)
        self.create_order_item_obj(data)
        return Response(status=status.HTTP_201_CREATED)
 

class OrderItemDetailView(OrderItemHelperMixin, APIView):
    model = OrderItem
    queryset = model.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsCustomer]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            if not user.groups.filter(name='Manager'):
                self.queryset = self.queryset.filter(user=user)
            order_item_obj = self.queryset.get(pk=kwargs['pk'])
            serialized_object = self.serializer_class(order_item_obj)
            return Response(serialized_object.data, status=status.HTTP_200_OK)
        except self.model.DoesNotExist:
            return Response({'message': 'object not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, *args, **kwargs):
        try:
            user = request.user
            if not user.groups.filter(name='Manager'):
                self.queryset = self.queryset.filter(user=user)
            if request.data.get('quantity') is not None:
                order_item_obj = self.queryset.get(pk=kwargs['pk'])
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
            user = request.user
            if not user.groups.filter(name='Manager'):
                self.queryset = self.queryset.filter(user=user)
            order_item_obj = self.queryset.get(pk=kwargs['pk'])
            order_item_obj.delete()
            return Response({}, status=status.HTTP_200_OK)
        except OrderItem.DoesNotExist:
            return Response({'message': 'object not found'})


class OrderListView(UserHelperMixin, OrderListHelperMixin, ListCreateAPIView):
    model = Order
    queryset = model.objects.all()
    serializer_class = OrderSerializer
    ordering_fields = ['user', 'delivery_crew', 'status', 'date']
    search_fields = ['user', 'delivery_crew', 'status', 'date']
    filterset_fields = ['user', 'delivery_crew', 'status', 'date']

    def check_permissions(self, request):
        if request.method in ['GET']:
            self.permission_classes = [IsCustomerOrDeliveryCrew]
        elif request.method in ['POST']:
            self.permission_classes = [IsCustomer]
        else:
            self.permission_classes = [IsManager]
        return super().check_permissions(request)

    def get(self, request, *args, **kwargs):
        if self.user_is_admin(request): pass
        elif self.user_is_manager(request): pass
        elif self.user_is_delivery_crew(request):
            self.queryset = self.queryset.filter(delivery_crew=request.user)
        elif self.user_is_customer(request):
            self.queryset = self.queryset.filter(user=request.user)
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


class OrderDetailView(UserHelperMixin, CommonUtilsMixin, RetrieveUpdateDestroyAPIView):
    model = Order
    queryset = model.objects.all()
    serializer_class = OrderSerializer

    def check_permissions(self, request):
        if request.method in ['GET']:
            self.permission_classes = [IsCustomerOrDeliveryCrew]
        elif request.method in ['PATCH']:
            self.permission_classes = [IsDeliveryCrew]
            if request.data.get('delivery_crew_id'):
                self.permission_classes = [IsManager]
        else:
            self.permission_classes = [IsManager]
        return super().check_permissions(request)
    
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.groups.filter(name='Manager'):
            pass #self.queryset = self.queryset
        elif user.groups.filter(name='Customer'):
            self.queryset = self.queryset.filter(user=user)
        elif user.groups.filter(name='Delivery Crew'):
            self.queryset = self.queryset.filter(delivery_crew=user)
        return super().get(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        status = request.data.get('status')
        delivery_crew_id = request.data.get('delivery_crew_id')
        try:
            if self.user_is_admin(request): pass
            elif self.user_is_manager(request): pass
            elif self.user_is_delivery_crew(request):
                self.queryset = self.queryset.filter(delivery_crew=request.user)
            order_object = self.queryset.get(pk=kwargs['pk'])
            if status is not None:
                if int(status) < 0 or int(status) > 1: raise ValueError
                order_object.status = int(status)
                order_object.save()
            if delivery_crew_id is not None:
                order_object.delivery_crew = User.objects.get(pk=delivery_crew_id)
                order_object.save()
            return self.object_serialized_response(request, order_object)
        except Purchase.DoesNotExist:
            return Response({'message': 'object not found'}, status=status.HTTP_404_BAD_REQUEST)
        except ValueError:
            return Response({'status': 'requires a valid integer (0 or 1)', 'id': 'requires a valid inetger'}, status=status.HTTP_400_BAD_REQUEST)


class PurchaseListView(ListAPIView):
    model = Purchase
    queryset = model.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsCustomer]
    ordering_fields = ['user', 'date']
    search_fields = ['user', 'date']
    filterset_fields = ['user', 'date']

    def get(self, request, *args, **kwargs):
        user = request.user
        self.queryset = self.queryset.filter(user=user)
        return super().get(request, *args, **kwargs)


class PurchaseDetailView(PurchaseDetailHelperMixin, RetrieveAPIView, DestroyAPIView):
    model = Purchase
    queryset = model.objects.all()
    serializer_class = PurchaseSerializer

    def check_permissions(self, request):
        if request.method in ['GET']:
            self.permission_classes = [IsCustomer]
        else:
            self.permission_classes = [IsManager]
        return super().check_permissions(request)
    
    def get(self, request, *args, **kwargs):
        user = request.user
        self.queryset = self.queryset.filter(user=user)
        return super().get(*args, **kwargs)


class PurchaseItemListView(ListAPIView):
    model = PurchaseItem
    queryset = model.objects.all()
    serializer_class = PurchaseItemSerializer
    permission_classes = [IsCustomer]
    ordering_fields = ['user', 'menuitem', 'price']
    search_fields = ['user', 'menuitem', 'price']
    filterset_fields = ['user', 'menuitem', 'price']

    def get(self, request, *args, **kwargs):
        user = request.user
        self.queryset = self.queryset.filter(user=user)
        return super().get(request, *args, **kwargs)


class PurchaseItemDetailView(RetrieveUpdateDestroyAPIView):
    model = PurchaseItem
    queryset = model.objects.all()
    serializer_class = PurchaseItemSerializer
    permission_classes = [IsCustomer]

    def check_permissions(self, request):
        if request.method in ['GET']:
            self.permission_classes = [IsCustomer]
        else:
            self.permission_classes = [IsManager]
        return super().check_permissions(request)

    def get(self, request, *args, **kwargs):
        user = request.user
        self.queryset = self.queryset.filter(user=user)
        return super().get(*args, **kwargs)