from django.contrib import admin
from django.urls import path
from contador_de_calorias import views 

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index , name="index"),
    path("deletar/<int:id>/", views.deletar_consumidos, name="deletar"),
    path("login/", views.login, name="login"),
    path("cadastro/", views.cadastro, name="cadastro"),
]
