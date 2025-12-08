from django.contrib import admin
from django.urls import path
from contador_de_calorias import views 

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index , name="index"),
]
