
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F
from django.urls import reverse
from .models import Questao, Alternativa
from .forms import QuestaoForm, AlternativaForm


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

def nova_enquete(request):
    if request.method == "POST":
        try:
            form = QuestaoForm(request.POST)
            if form.is_valid():
                # salva questao mas não envia ao banco ainda (commit=False)
                # para podermos definir a data de publicação via código
                questao = form.save(commit=False)
                questao.data_pub = timezone.now()
                questao.save()
                return redirect('equetes:index')
        except Exception as e:
            form.add_error(None,f"Ocorreu um erro inesperado. {e}")
    else:
        form = QuestaoForm()
        
    return render(request, 'equetes/cadastro.html', {'form': form})

'''def nova_alternativa(request, questao_id):
    questao = get_object_or_404(Questao, pk= questao_id)
    if request.method == "POST":
        try:
            form = AlternativaForm(request.POST)
            if form.is_valid():
                alternativa = form.save(commit=False)
                alternativa.questao = questao
                alternativa.save()
            return redirect('equetes:index')'''