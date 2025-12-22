from django.db import models
from django.contrib.auth.models import User

class Alimentos(models.Model):

    nome = models.CharField(max_length=120)
    carboidratos = models.FloatField()
    proteinas = models.FloatField()
    gorduras = models.FloatField()

    def __str__(self):
        return self.nome
    
    @property
    def calorias(self):
        return (self.carboidratos * 4 + self.proteinas * 4 + self.gorduras * 9)

class AlimentoIngerido(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    alimento_ingerido = models.ForeignKey(Alimentos, on_delete=models.CASCADE)

class Perfil(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    meta_calorias = models.IntegerField(default=2500)
    
    def __str__(self):
        return self.user.username
    

