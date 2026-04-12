from django.urls import path

from . import views

urlpatterns = [
    path(
        route='stories/',
        view=views.HistoryListView.as_view(),
        name='history_list'
    ),
    path(
        route='stories/create/',
        view=views.HistoryCreateView.as_view(),
        name='history_create',
    ),
    path(
        route='stories/<int:pk>/update/',
        view=views.HistoryUpdateView.as_view(),
        name='history_update',
    ),
    path(
        route='stories/<int:pk>/delete/',
        view=views.HistoryDeleteView.as_view(),
        name='history_delete',
    ),
]
