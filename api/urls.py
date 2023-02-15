from django.urls import path

from .views import (
    UserDetailView, UserListView,
    GroupListViewSet, GroupDetailView,
    SysAdminListView, SysAdminDetailViewSet,
    ManagerListView, ManagerDetailView,
    DeliveryCrewListView, DeliveryCrewDetailView,
    CustomerListView, CustomerDetailView,
    MenuItemListView, MenuItemDetailView,
    CategoryListView, CategoryDetailView, CategoryMenuItemsView,
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
    path('groups/admins', SysAdminListView.as_view()),
    path('groups/admins/<int:pk>', SysAdminDetailViewSet.as_view()),
    path('groups/managers', ManagerListView.as_view()),
    path('groups/managers/<int:pk>', ManagerDetailView.as_view()),
    path('groups/delivery-crew', DeliveryCrewListView.as_view()),
    path('groups/delivery-crew/<int:pk>', DeliveryCrewDetailView.as_view()),
    path('groups/customers', CustomerListView.as_view()),
    path('groups/customers/<int:pk>', CustomerDetailView.as_view()),

    path('menu-items', MenuItemListView.as_view(LIST)),
    path('menu-items/<int:pk>', MenuItemDetailView.as_view(DETAIL), name='menuitem-detail'),
    path('categories', CategoryListView.as_view(LIST)),
    path('categories/<int:pk>', CategoryDetailView.as_view(DETAIL), name='category-detail'),
    path('categories/<int:pk>/menu-items', CategoryMenuItemsView.as_view()),
    path('order-items', OrderItemListView.as_view()),
    path('order-items/<int:pk>', OrderItemDetailView.as_view(), name='orderitem-detail'),

    path('cart', CartView.as_view()),

    path('orders', OrderListView.as_view()),
    path('orders/<int:pk>', OrderDetailView.as_view(), name='order-detail'),

    path('purchases', PurchaseListView.as_view()),
    path('purchases/<int:pk>', PurchaseDetailView.as_view(), name='purchase-detail'),

    path('purchase-items', PurchaseListView.as_view()),
    path('purchase-items/<int:pk>', PurchaseDetailView.as_view(), name='purchaseitem-detail'),
]