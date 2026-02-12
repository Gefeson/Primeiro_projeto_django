from urllib import request
from django.shortcuts import get_object_or_404, render 
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F
from django.urls import reverse
from equetes.models import Questao, Alternativa


def index(request):
    lista_questoes_recentes = Questao.objects.order_by("-data_pub")[:5]
    contexto = {"lista_questoes_recentes": lista_questoes_recentes}
    return render(request, "equetes/index.html", contexto)

def detalhes(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, "equetes/detalhes.html", {"questao": questao})

def voto(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    try:
        #tenta capturar o ID da alternativa vinda do questionario
        selecionada = questao.alternativa_set.get(pk=request.POST['alternativa'])
    except(KeyError, Alternativa.DoesNotExist):
        # Se 'alternativa' não estiver no POST, exibe o formulário novamente com erro 
        return render(request, 'equetes/detalhes.html',{'questao':questao,'error_message':"Você não selecionou uma opção válida"})
    else:
        #Incrementa o voto de forma segura no banco de dados
        selecionada.votos = F('votos') + 1
        selecionada.save()
        
        # Redireciona para a página de resultados após o sucesso 
        # Isso evita que o usuário vote duas vezes se clicar em "Atualizar" no navegador 
    return HttpResponseRedirect(reverse('equetes:resultados', args=(questao.id,))) 

def resultados(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'equetes/resultados.html', {'questao':questao})
    