from django.shortcuts import render
from .models import Alimentos

def index(request):
    alimento = Alimentos.objects.all()
    return render(request, "contador_de_calorias/index.html", {"alimento":alimento})

