from django.urls import path

from . import views

urlpatterns = [
    path(
        route='classification',
        view=views.SkuListView.as_view(),
        name='classification'
    ),
]
