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

from .helpers import user_is_requested_user
from .mixins import RetrieveUpdateDestroyAPIViewMixin


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


class GroupListViewSet(ModelViewSet):
    model = Group
    queryset = model.objects.all()
    serializer_class = GroupSerializer

    def check_permissions(self, request):
        if request.method in ['GET']:
            self.permission_classes = [IsManager]
        else:
            self.permission_classes = []
        return super().check_permissions(request)


class GroupDetailView(ModelViewSet):
    model = Group
    queryset = model.objects.all()
    serializer_class = GroupSerializer

    def check_permissions(self, request):
        if request.method in ['GET']:
            self.permission_classes = [IsManager]
        else:
            requested_group_pk = request.parser_context['kwargs'].get('pk')
            if Group.objects.get(pk=requested_group_pk).name in ['Manager', 'SysAdmin']:
                self.permission_classes = [IsSystemAdministrotor]
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


class ManagerDetailViewSet(ModelViewSet):
    model = User
    queryset = User.objects.filter(groups__name='Manager').exclude(groups__name='SysAdmin')
    serializer_class = UserSerializer

    def check_permissions(self, request):
        if request.method in ['GET', 'PATCH', 'PUT', 'DELETE']:
            if user_is_requested_user(request):
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
    

class DeliveryCrewDetailViewSet(ModelViewSet):
    model = User
    queryset = User.objects.filter(groups__name='Delivery Crew').exclude(groups__name='SysAdmin').exclude(groups__name='Manager')
    serializer_class = UserSerializer

    def check_permissions(self, request):
        if user_is_requested_user(request):
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

class CustomerDetailViewSet(ModelViewSet):
    model = User
    queryset = User.objects.filter(groups__name='Customer').exclude(groups__name='SysAdmin').exclude(groups__name='Manager')
    serializer_class = UserSerializer

    def check_permissions(self, request):
        if user_is_requested_user(request):
            self.permission_classes = [IsCustomer]
        else:
            self.permission_classes = [IsManager]
        return super().check_permissions(request)


class CategoryListViewSet(ModelViewSet):
    model = Category
    queryset = model.objects.all()
    serializer_class = CategorySerializer

    def check_permissions(self, request):
        if not request.method in ['GET']:
            self.permission_classes = [IsManager]
        else:
            self.permission_classes = {IsCustomer}
        return super().check_permissions(request)


class CategoryDetailViewSet(ModelViewSet):
    model = Category
    queryset = model.objects.all()
    serializer_class = CategorySerializer

    def check_permissions(self, request):
        if not request.method in ['GET']:
            self.permission_classes = [IsManager]
        else:
            self.permission_classes = {IsCustomer}
        return super().check_permissions(request)


class MenuItemListViewSet(ModelViewSet):
    model = MenuItem
    queryset = model.objects.all()
    serializer_class = MenuItemSerializer

    def check_permissions(self, request):
        if not request.method in ['GET']:
            self.permission_classes = [IsManager]
        else:
            self.permission_classes = [IsCustomer]
        return super().check_permissions(request)


class MenuItemDetailViewSet(ModelViewSet):
    model = MenuItem
    queryset = model.objects.all()
    serializer_class = MenuItemSerializer

    def check_permissions(self, request):
        if not request.method in ['GET']:
            self.permission_classes = [IsManager]
        else:
            self.permission_classes = [IsCustomer]
        return super().check_permissions(request)


class OrderItemListViewSet(ListCreateAPIView, DestroyAPIView):
    model = OrderItem
    related_model = MenuItem
    queryset = model.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsCustomer]

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
        
    def delete(self, request, *args, **kwargs):
        try:
            if not request.data.get('id') is None:
                instance = self.queryset.filter(user=request.user).get(pk=request.data.get('id'))
                instance.delete()
            else:
                self.queryset.filter(user=request.user).delete()
            return self.get(request)
        except self.model.DoesNotExist:
            return Response({'message': 'object not found'}, status=status.HTTP_404_NOT_FOUND)


class OrderItemDetailViewSet(RetrieveAPIView):
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
    

class CartViewSet(RetrieveUpdateDestroyAPIView):
    model = Cart
    queryset = model.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsCustomer]
    related_model = OrderItem

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
    

class OrderListViewSet(ListCreateAPIView):
    model = Order
    queryset = model.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsCustomer]

    def get_user_cart(self, request):
        try:
            return Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return None
    
    def create_purchase_record(self, request):
        # try:
        user_cart = self.get_user_cart(request)
        purchase = Purchase.objects.create(user=request.user)
        purchase.orderitems.set(user_cart.orderitems.all())
        purchase.save()
        return purchase
        # except:
        #     return None
    
    def get_purchase_cost(self, purchase_record):
        total_cost = 0
        for orderidem in purchase_record.orderitems.all():
            total_cost += orderidem.price
        return total_cost

    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(user=request.user)
        return super().get(request, *args, **kwargs)
    
    def post(self, request):
        """
        Take all orderitems present in the Cart table and place them in a new Purchase instance
        relate that Purchase instance to a new Order instance
        """
        user_cart = self.get_user_cart(request)
        purchase_record = self.create_purchase_record(request)
        if purchase_record is None:
            return Response({'message': 'Error'}, status=status.HTTP_400_BAD_REQUEST)
        order_object = self.model.objects.create(
            user = request.user,
            purchase = purchase_record,
            total = self.get_purchase_cost(purchase_record)
        )
        user_cart.orderitems.clear()
        order_object.save()
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
