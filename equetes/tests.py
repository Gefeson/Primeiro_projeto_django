from django.utils import timezone
import datetime
from django.test import TestCase
from .models import Alternativa, Questao, Voto
from django.contrib.auth.models import User

class QuestaoModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username = "testuser")
        
    def test_foi_publicada_recentemente_com_questao_no_futuro(self):
        tempo = timezone.now() + timezone.timedelta(days=30)
        questao_futuro = Questao(descricao="Futuro?", data_pub=tempo, usuario=self.user)
        self.assertIs(questao_futuro.foi_publicada_recentemente(), False)
        
    def test_foi_publicada_recentemente_com_questao_no_futuro(self):
        time = timezone.now() + timezone.timedelta(days=30)
        old_question = Questao(descricao ="Questao antiga.", data_pub=time, usuario=self.user)
        
        
    def test_total_votos_calcula_corretamente(self):
        """
        A propertytotal_votosdeve retornar a contagem exata de objetos Voto.
        """
        q = Questao.objects.create(descricao="Qual sua cor?", data_pub=timezone.now(), usuario=self.user)
        alt= Alternativa.objects.create(questao=q, descricao="Azul")
        # Criando votos manuais
        Voto.objects.create(usuario=self.user, questao=q,  alternativa=alt)
        self.assertEqual(alt.total_votos, 1)
        
class VotoViewTests(TestCase):
    def test_impedir_duplo_voto(self):
    # Setup: Criar user, questão e alternativa
    # Executar POST de voto duas vezes
    # Verificar se a mensagem de erro aparece no contexto
        pass

class EnquetesViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='votante', password='123')
        self.dono = User.objects.create_user(username='dono', password='123')
        self.questao = Questao.objects.create(
            descricao="Questão Teste",
            data_pub=timezone.now(),
            usuario=self.dono
            )
        self.alt = Alternativa.objects.create(questao=self.questao, descricao="Alt 1")

    def test_voto_sem_login_redireciona(self):
        """Usuário não logado deve ser redirecionado para a página de login ao tentar votar."""
        response = self.client.post(f'/equetes/{self.questao.id}/voto/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
        
    def test_voto_duplicado_gera_erro(self):
        """Usuário não pode votar duas vezes na mesma questão."""
        self.client.login(username='votante', password='123')
        # Primeiro voto
        self.client.post(f'/equetes/{self.questao.id}/voto/', {'alternativa': self.alt.id})
        # Segundo voto (mesma questão)
        response = self.client.post(f'/equetes/{self.questao.id}/voto/', {'alternativa': self.alt.id}) 
        
        self.assertContains(response, "Você já participou desta enquete.")
        self.assertEqual(Voto.objects.filter(questao=self.questao).count(), 1)  

    def test_excluir_alternativa_alheia_proibido(self):
        """Um usuário não pode excluir alternativas de uma questão que não criou."""
        self.client.login(username='votante', password='123') # Logado com quem  não é o dono
        response = self.client.post(f'/equetes/alternativa/{self.alt.id}/excluir/')
        # Deve retornar 403 Forbidden conforme definido na sua View
        self.assertEqual(response.status_code, 403)