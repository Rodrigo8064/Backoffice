from django.urls import path
from . import views


urlpatterns = [
    path('classification', views.SkuListView.as_view(), name='classification'),
    path('agent', views.ia_agent, name='agente_ia'),
]