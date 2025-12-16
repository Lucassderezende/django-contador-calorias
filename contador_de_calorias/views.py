from django.shortcuts import render
from .models import Alimentos, AlimentoIngerido
from django.shortcuts import get_object_or_404

def index(request):

        alimentos = Alimentos.objects.all()

        if request.method == "POST":
            alimento_ingerido = request.POST["alimento_consumido"]
            alimento = get_object_or_404(Alimentos, nome=alimento_ingerido)
            registro = AlimentoIngerido(user=request.user, alimento_ingerido=alimento)
            registro.save()
        alimentos_registrados = AlimentoIngerido.objects.filter(user=request.user)
        return render(request, "contador_de_calorias/index.html", {"alimentos":alimentos, "alimentos_registrados":alimentos_registrados})