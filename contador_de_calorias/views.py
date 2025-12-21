from django.shortcuts import render, get_object_or_404, redirect
from .models import Alimentos, AlimentoIngerido
from django.contrib.auth.decorators import login_required

@login_required
def index(request):

    alimentos = Alimentos.objects.all()

    if request.method == "POST":
        alimento_nome = request.POST["alimento_consumido"]
        alimento = get_object_or_404(Alimentos, nome=alimento_nome)
        AlimentoIngerido.objects.create(
            user = request.user,
            alimento_ingerido = alimento
        )

    alimentos_registrados = AlimentoIngerido.objects.filter(user=request.user)

    total_carboidratos = sum(
       a.alimento_ingerido.carboidratos for a in alimentos_registrados
    )

    total_proteinas = sum(
        a.alimento_ingerido.proteinas for a in alimentos_registrados
    )

    total_gorduras = sum(
        a.alimento_ingerido.gorduras for a in alimentos_registrados
    )

    total_calorias = sum(
        a.alimento_ingerido.calorias for a in alimentos_registrados
    )

    kcalCarb = total_carboidratos * 4;
    kcalProt = total_proteinas * 4;
    kcalGord = total_gorduras * 9;

    totalKcal = kcalCarb + kcalProt + kcalGord;

    porcCarb = round((kcalCarb / totalKcal) * 100, 2) if totalKcal else 0
    porcProt = round((kcalProt / totalKcal) * 100, 2) if totalKcal else 0
    porcGord  = round((kcalGord / totalKcal) * 100, 2) if totalKcal else 0

    meta = 2500
    porcentagem = round((totalKcal / meta) * 100, 2) if meta else 0

    contexto = {
        "alimentos": alimentos,
        "alimentos_registrados": alimentos_registrados,
        "total_carboidratos": round(total_carboidratos, 2),
        "total_proteinas": round(total_proteinas, 2),
        "total_gorduras": round(total_gorduras, 2),
        "total_calorias": total_calorias,
        "kcalCarb": kcalCarb,
        "kcalProt": kcalProt,
        "kcalGord": kcalGord,
        "totalKcal": totalKcal,
        "porcCarb": porcCarb,
        "porcProt": porcProt,
        "porcGord": porcGord,
        "porcentagem": porcentagem
    }

    return render(request, "contador_de_calorias/index.html", contexto)

@login_required
def deletar_consumidos(request, id):
    alimento = get_object_or_404(AlimentoIngerido,id=id,user=request.user)
    
    if request.method == "POST":
        alimento.delete()

    return redirect("index")

def login(request):

    return render(request, "login.html")

def logout(request):

    return render(request, "logout.html")