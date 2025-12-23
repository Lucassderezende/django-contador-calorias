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
from django.db.models.signals import post_save
from django.dispatch import receiver


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

    kcalCarb = total_carboidratos * 4
    kcalProt = total_proteinas * 4
    kcalGord = total_gorduras * 9

    totalKcal = kcalCarb + kcalProt + kcalGord

    porcCarb = (kcalCarb / totalKcal) * 100 if totalKcal else 0
    porcProt = (kcalProt / totalKcal) * 100 if totalKcal else 0
    porcGord  = (kcalGord / totalKcal) * 100 if totalKcal else 0

    meta = request.user.perfil.meta_calorias
    porcentagem = min(round((totalKcal / meta) * 100, 2), 100) if meta else 0

    contexto = {
        "alimentos": alimentos,
        "alimentos_registrados": alimentos_registrados,
        "total_carboidratos": round(total_carboidratos, 2),
        "total_proteinas": round(total_proteinas, 2),
        "total_gorduras": round(total_gorduras, 2),
        "kcalCarb": float(kcalCarb),
        "kcalProt": float(kcalProt),
        "kcalGord": float(kcalGord),
        "totalKcal": totalKcal,
        "porcCarb": porcCarb,
        "porcProt": porcProt,
        "porcGord": porcGord,
        "porcentagem": porcentagem,
        "meta": meta
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
    
@login_required(login_url="login")
def definir_meta(request):
    if request.method == "POST":
        meta = int(request.POST.get("meta"))
        perfil = request.user.perfil
        perfil.meta_calorias = meta
        perfil.save()
        messages.success(request, "Meta de calorias atualizada!")
        return redirect("index")

@login_required(login_url="login")
def deletar_todos_consumidos(request):
    
    if request.method == "POST":
        AlimentoIngerido.objects.filter(user=request.user).delete()
        messages.success(request, "Todos os itens foram removidos!")
    return redirect("index")