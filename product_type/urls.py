from django.urls import path

from . import views

urlpatterns = [
    path(
        route='products/list/',
        view=views.ProductListView.as_view(),
        name='product_list'
    ),
    path(
        route='products/create/',
        view=views.ProductCreateView.as_view(),
        name='product_create',
    ),
    path(
        route='products/<int:pk>/update/',
        view=views.ProductUpdateView.as_view(),
        name='product_update',
    ),
    path(
        route='products/<int:pk>/delete/',
        view=views.ProductDeleteView.as_view(),
        name='product_delete',
    ),
]
