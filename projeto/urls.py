from django.contrib import admin
from django.urls import path
from contador_de_calorias import views 

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index , name="index"),
    path("deletar/<int:id>/", views.deletar_consumidos, name="deletar"),
    path("login/", views.login, name="login"),
    path("cadastro/", views.cadastro, name="cadastro"),
    path("desconectar/", views.desconectar_usuario, name="desconectar_usuario"),
    path("definir-meta/", views.definir_meta, name="definir_meta"),
    path("deletar_itens/", views.deletar_todos_consumidos, name="deletar_consumidos"),
]
