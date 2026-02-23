'''from django.utils import timezone
import datetime
from django.test import TestCase
from .models import Questao
from django.contrib.auth.models import User

class QuestaoModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username = "testuser")
        
    def test_foi_publicada_recentemente_com_questao_no_futuro(self):
        tempo = timezone.now() + timezone.timedelta(days=30)
        questao_futuro = Questao(descricao="futuro?", data_pub=tempo, usuario=self.user)
        self.assertIs(questao_futuro.foi_publicada_recentemente(), False)
        
    def test_foi_publicada_recentemente_com_questao_no_futuro(self):
        time = timezone.now() + timezone.timedelta(days=30)
        old_question = Questao(descricao ="Questao antiga.", data_pub=tempo, usuario=self.user)'''
        