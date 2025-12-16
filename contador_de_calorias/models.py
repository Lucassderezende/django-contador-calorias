from django.db import models
from django.contrib.auth.models import User

class Alimentos(models.Model):

    nome = models.CharField(max_length=120)
    carboidratos = models.FloatField()
    proteinas = models.FloatField()
    gorduras = models.FloatField()
    calorias = models.IntegerField()

    def __str__(self):
        return self.nome

class AlimentoIngerido(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    alimento_ingerido = models.ForeignKey(Alimentos, on_delete=models.CASCADE)


