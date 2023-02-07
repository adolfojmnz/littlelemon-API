from django.urls import path

from .views import (
    UserDetailView,
    GroupListViewSet, GroupDetailView,
    SysAdminListViewSet, SysAdminDetailViewSet,
    ManagerListViewSet, ManagerDetailViewSet,
    DeliveryCrewListViewSet, DeliveryCrewDetailViewSet,
    CustomerListViewSet, CustomerDetailViewSet,
    MenuItemListViewSet, MenuItemDetailViewSet,
    CategoryListViewSet, CategoryDetailViewSet,
    OrderItemListViewSet,
    OrderItemDetailViewSet,
    CartViewSet,
    OrderListViewSet,
    OrderDetailViewSet,
    PurchaseListView,
    PurchaseDetailView,
)

LIST = {'get': 'list', 'post': 'create'}
DETAIL = {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}


urlpatterns = [
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

    path('cart', CartViewSet.as_view()),

    path('order-items', OrderItemListViewSet.as_view()),
    path('order-items/<int:pk>', OrderItemDetailViewSet.as_view(), name='orderitem-detail'),

    path('purchases', PurchaseListView().as_view()),
    path('purchases/<int:pk>', PurchaseDetailView().as_view(), name='purchase-detail'),

    path('orders', OrderListViewSet.as_view()),
    path('orders/<int:pk>', OrderDetailViewSet.as_view(DETAIL)),
]