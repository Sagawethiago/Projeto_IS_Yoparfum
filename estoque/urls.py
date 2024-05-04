from django.urls import path
from . import views
from .views import ProdutoList
from .views import index

from django.urls import path
from .views import minha_view

urlpatterns = [
    path('add_produto/', views.add_produto, name="add_produto"),
    path('list_produtos/', views.list_produtos, name='list_produtos'),
    path('produto/', views.produto, name="produto"),
    path('api/produtos/', ProdutoList.as_view(), name='api_produtos'),
    path('', index, name='home'),
    path('apivz/', views.minha_view, name='minha_view'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
]

