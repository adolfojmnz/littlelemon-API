from django.urls import path

from .views import (
    UserDetailView, UserListView,
    GroupListViewSet, GroupDetailView,
    SysAdminListViewSet, SysAdminDetailViewSet,
    ManagerListViewSet, ManagerDetailViewSet,
    DeliveryCrewListViewSet, DeliveryCrewDetailViewSet,
    CustomerListViewSet, CustomerDetailViewSet,
    MenuItemListViewSet, MenuItemDetailViewSet,
    CategoryListViewSet, CategoryDetailViewSet,
    OrderItemListView, OrderItemDetailView,
    CartView,
    OrderListView, OrderDetailView,
    PurchaseListView, PurchaseDetailView,
)

LIST = {'get': 'list', 'post': 'create'}
DETAIL = {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}


urlpatterns = [
    path('users', UserListView.as_view()),
    path('users/<int:pk>', UserDetailView.as_view(), name='user-detail'),

    path('groups', GroupListViewSet.as_view()),
    path('groups/<int:pk>', GroupDetailView.as_view(DETAIL)),
    path('groups/admins', SysAdminListViewSet.as_view(LIST)),
    path('groups/admins/<int:pk>', SysAdminDetailViewSet.as_view(DETAIL)),
    path('groups/managers', ManagerListViewSet.as_view()),
    path('groups/managers/<int:pk>', ManagerDetailViewSet.as_view(DETAIL)),
    path('groups/delivery-crew', DeliveryCrewListViewSet.as_view()),
    path('groups/delivery-crew/<int:pk>', DeliveryCrewDetailViewSet.as_view(DETAIL)),
    path('groups/customers', CustomerListViewSet.as_view(LIST)),
    path('groups/customers/<int:pk>', CustomerDetailViewSet.as_view(DETAIL)),

    path('menu-items', MenuItemListViewSet.as_view(LIST)),
    path('menu-items/<int:pk>', MenuItemDetailViewSet.as_view(DETAIL), name='menuitem-detail'),
    path('categories', CategoryListViewSet.as_view(LIST)),
    path('categories/<int:pk>', CategoryDetailViewSet.as_view(DETAIL), name='category-detail'),

    path('cart', CartView.as_view()),
    path('order-items', OrderItemListView.as_view()),
    path('order-items/<int:pk>', OrderItemDetailView.as_view(), name='orderitem-detail'),

    path('orders', OrderListView.as_view()),
    path('orders/<int:pk>', OrderDetailView.as_view(), name='order-detail'),

    path('purchases', PurchaseListView.as_view()),
    path('purchases/<int:pk>', PurchaseDetailView.as_view(), name='purchase-detail'),

    path('purchase-items', PurchaseListView.as_view()),
    path('purchase-items/<int:pk>', PurchaseDetailView.as_view(), name='purchase-detail'),
]