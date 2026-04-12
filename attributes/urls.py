from django.urls import path

from . import views

urlpatterns = [
    path(
        route='attributes/list/',
        view=views.AttributeListView.as_view(),
        name='attribute_list',
    ),
    path(
        route='attributes/create/',
        view=views.AttributeCreateView.as_view(),
        name='attribute_create',
    ),
    path(
        route='attributes/<int:pk>/update/',
        view=views.AttributeUpdateView.as_view(),
        name='attribute_update',
    ),
    path(
        route='attributes/<int:pk>/',
        view=views.AttributeDetailView.as_view(),
        name='attribute_detail',
    ),
]
