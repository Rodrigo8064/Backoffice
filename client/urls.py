from django.urls import path
from . import views


urlpatterns = [
    path('classification', views.SkuListView.as_view(), name='classification'),
]