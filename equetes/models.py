from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Questao(models.Model):
    descricao = models.CharField(max_length=200)
    data_pub = models.DateTimeField("Data de publicação")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name ="minhas_questoes")
    
    def __str__(self):
        return self.descricao
    
    class Meta:
        verbose_name = "Questão"
        verbose_name_plural = "Questões"
    
class Alternativa(models.Model):
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=200)
    #votos = models.IntegerField(default=0) substitudo pelo total_votos()
    
    def __str__(self):
        return f"{self.questao.descricao} - {self.descricao}"
    class Meta:
        verbose_name = "Alternativa"
        verbose_name_plural = "Alternativas"
        
    @property
    def total_votos(self):
    # Conta quantos objetos Voto estão relacionados a esta alternativa
        return self.voto_set.count()
        
        
def foi_publicada_recentemente(self):
    agora = timezone.now()
    return agora - timezone.timedelta(days=1) <= self.data_pub <= agora

class Voto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    alternativa = models.ForeignKey(Alternativa, on_delete=models.CASCADE)
    data_voto = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        #Esta regra impede que um mesmo ususario tenha dois registros para uma mesma questão
        unique_together = ('usuario', 'questao')
        