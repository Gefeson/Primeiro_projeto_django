from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from equetes.models import Questao

def index(request):
    lista_questoes_recentes = Questao.objects.order_by("-data_pub")[:5]
    contexto = {"lista_questoes_recentes": lista_questoes_recentes}
    return render(request, "equetes/index.html", contexto)

def detalhe(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, "equetes/detalhes.html", {"questao": questao})

def voto(request, questao_id):
    return HttpResponse(f"Você está votando na Questão {questao_id}.")

def resultado(request, questao_id):
    return HttpResponse(f"Você está vendo os resultados da Questão {questao_id}.")
