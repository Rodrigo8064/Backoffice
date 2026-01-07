from django.urls import path
from . import views


urlpatterns = [
    path('stories/', views.HistoryListView.as_view(), name='history'),
]