from django.shortcuts import render
from .models import Alimentos, AlimentoIngerido
from django.shortcuts import get_object_or_404
from django.contrib import messages

def index(request):

    if request.method == "POST":
        alimento_ingerido = request.POST["alimento_consumido"]
        alimento = get_object_or_404(Alimentos, nome=alimento_ingerido)
        user = request.user
        registro = AlimentoIngerido(user=user, alimento_ingerido=alimento)
        registro.save()
        alimentos = Alimentos.objects.all()
        return render(request, "contador_de_calorias/index.html", {"alimentos":alimentos})
    else:
        alimentos = Alimentos.objects.all()
        return render(request, "contador_de_calorias/index.html", {"alimentos":alimentos})


