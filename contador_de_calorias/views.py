from django.shortcuts import render, get_object_or_404, redirect
from .models import Alimentos, AlimentoIngerido
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_django
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

@login_required(login_url="login")
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

    kcalCarb = round(total_carboidratos * 4, 1)
    kcalProt = round(total_proteinas * 4, 1)
    kcalGord = round(total_gorduras * 9, 1)

    totalKcal = round(kcalCarb + kcalProt + kcalGord)

    porcCarb = round((kcalCarb / totalKcal) * 100, 2) if totalKcal else 0
    porcProt = round((kcalProt / totalKcal) * 100, 2) if totalKcal else 0
    porcGord  = round((kcalGord / totalKcal) * 100, 2) if totalKcal else 0

    meta = 2500
    porcentagem = min(round((totalKcal / meta) * 100, 2), 100) if meta else 0

    contexto = {
        "alimentos": alimentos,
        "alimentos_registrados": alimentos_registrados,
        "total_carboidratos": round(total_carboidratos, 2),
        "total_proteinas": round(total_proteinas, 2),
        "total_gorduras": round(total_gorduras, 2),
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

@login_required(login_url="login")
def deletar_consumidos(request, id):
    alimento = get_object_or_404(AlimentoIngerido,id=id,user=request.user)
    
    if request.method == "POST":
        alimento.delete()

    return redirect("index")

def login(request):
    
    if request.method == "GET":
        return render(request, "login.html")
    
    username = request.POST.get("username")
    senha = request.POST.get("senha")
        
    if not username or not senha:
        messages.error(request, "Preencha todos os campos.")
        return redirect("login")
        
    user = authenticate(username=username, password=senha)
        
    if user is not None:
        login_django(request, user)
        messages.success(request, "Login realizado com sucesso!")
        return redirect("index")
    
    messages.error(request, "Usuário ou senha inválidos.")
    return redirect("login")
        

def cadastro(request):

    if request.method == "GET":
        return render(request, "cadastro.html")
    
    username = request.POST.get("username")
    email = request.POST.get("email")
    senha = request.POST.get("senha")
    
    if not username or not email or not senha:
        messages.error(request, "Preencha todos os campos.")
        return redirect("cadastro")
    
    if " " in username:
        messages.error(request, "O usuário não pode conter espaços.")
        return redirect("cadastro")

    
    if User.objects.filter(username=username).exists():
        messages.error(request, "Esse nome de usuário já existe.")
        return redirect("cadastro")
    
    try:
        validate_email(email)
    except ValidationError:
        messages.error(request, "Digite um e-mail válido.")
        return redirect("cadastro")
    
    if User.objects.filter(email=email).exists():
        messages.error(request, "Este e-mail já está cadastrado.")
        return redirect("cadastro")
    
    try:
        validate_password(senha)
    except ValidationError as e:
        for erro in e.messages:
            messages.error(request, erro)
        return redirect("cadastro")
              
    User.objects.create_user(username=username, email=email, password=senha)
        
    messages.success(request, "Usuário criado com sucesso! Faça login.")
    return redirect("login")
        
@login_required(login_url="login")
def desconectar_usuario(request):
    
    if request.method == "POST":
        list(messages.get_messages(request))
        logout(request)
        messages.success(request, "Usuário desconectado!")
        return redirect("login")