"""
URL configuration for projetodjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from estoqueDI import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('lista_itens/', views.lista_itens, name='lista_itens'),
    path('adicionar_itens/', views.adicionar_itens, name='adicionar_itens'),
    path('atualizar_itens/<str:pk>/',
         views.atualizar_itens, name='atualizar_itens'),
    path('delete_itens/<str:pk>/', views.delete_itens, name='delete_itens'),
    path('detalhe_estoque/<str:pk>/',
         views.detalhe_estoque, name='detalhe_estoque'),
    path('saida_items/<str:pk>/', views.saida_items, name='saida_items'),
    path('entrada_items/<str:pk>/', views.entrada_items, name='entrada_items'),
    path('reorderlevel/<str:pk>/', views.reorderlevel, name='reorderlevel'),
    path('admin/', admin.site.urls),

]
