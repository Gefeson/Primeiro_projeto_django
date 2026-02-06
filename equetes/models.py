from django.db import models

# Create your models here.
class Questao(models.Model):
    descricao = models.CharField(max_length=200)
    data_pub = models.DateTimeField("Data de publicação")
    
    def __str__(self):
        return self.descricao
    
    class Meta:
        verbose_name = "Questão"
        verbose_name_plural = "Questões"
    
class Alternativa(models.Model):
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Alternativa"
        verbose_name_plural = "Alternativas"