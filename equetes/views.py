
from django.shortcuts import get_object_or_404, render 
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F
from django.urls import reverse
from .models import Questao, Alternativa


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
        alternativa_id = request.POST["alternativa"]
        selecionada = questao.alternativa_set.get(pk=alternativa_id)
    except (KeyError, Alternativa.DoesNotExist):
        return render(request, "equetes/detalhes.html", {
            "questao": questao,
            "error_message": "Você não selecionou uma opção válida"
        })

    Alternativa.objects.filter(pk=selecionada.pk).update(votos=F("votos") + 1)
    return HttpResponseRedirect(reverse("equetes:resultados", args=(questao.id,)))
 

def resultados(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'equetes/resultados.html', {'questao':questao})
    