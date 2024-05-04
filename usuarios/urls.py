from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome_page, name="welcome_page"),  # URL para a página de boas-vindas
    path('cadastrar_vendedor/', views.cadastrar_vendedor, name="cadastrar_vendedor"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),  # Corrigido para 'logout'
    path('excluir_usuario/<str:id>/', views.excluir_usuario, name="excluir_usuario"),
    path('cadastrar_produto/', views.cadastrar_produto, name="cadastrar_produto"),  # URL para cadastrar produtos
    path('consultar_estoque/', views.consultar_estoque, name="consultar_estoque"),  # URL para consultar estoque
    path('dashboard/', views.dashboard, name='dashboard'),  # URL para o dashboard
    path('api/produtos/', views.api_produtos, name='api_produtos'),
]