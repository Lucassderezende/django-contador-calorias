from django.db import models

class Alimentos(models.Model):

    def __str__(self):
        return self.nome
    

    nome = models.CharField(max_length=120)
    carboidratos = models.FloatField()
    proteinas = models.FloatField()
    gorduras = models.FloatField()
    calorias = models.IntegerField()


    