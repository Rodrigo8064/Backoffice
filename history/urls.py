from django.urls import path
from . import views


urlpatterns = [
    path('stories/', views.HistoryListView.as_view(), name='history_list'),
    path('stories/create/', views.HistoryCreateView.as_view(), name='history_create'),
    path('stories/<int:pk>/update/', views.HistoryUpdateView.as_view(), name='history_update'),
    path('stories/<int:pk>/delete/', views.HistoryDeleteView.as_view(), name='history_delete'),
]
