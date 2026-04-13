from django.urls import path

from . import views

urlpatterns = [
    path(
        route='categories/list/',
        view=views.CategoryListView.as_view(),
        name='category_list',
    ),
    path(
        route='categories/create/',
        view=views.CategoryCreateView.as_view(),
        name='category_create',
    ),
    path(
        route='categories/<int:pk>/update/',
        view=views.CategoryUpdateView.as_view(),
        name='category_update',
    ),
    path(
        route='categories/<int:pk>/delete/',
        view=views.CategoryDeleteView.as_view(),
        name='category_delete',
    ),
]
