
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
    #Criando uma instancia vazia no formulário
    form_alternativa = AlternativaForm()
    contexto = {
        'questao':questao,
        'form_alternativa':form_alternativa
    }
    
    return render(request, "equetes/detalhes.html", contexto)

def voto(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    try:
    # Tenta capturar o ID da alternativa vindo do formulário
        selecionada = questao.alternativa_set.get(pk=request.POST['alternativa'])
    except (KeyError, Alternativa.DoesNotExist):
    # Se 'alternativa' não estiver no POST, exibe o formulário novamente com erro
        return render(request, 'equetes/detalhes.html', {
            'questao': questao,
            'error_message': "Você não selecionou uma opção válida.",
            })
    else:
    # Incrementa o voto de forma segura no banco de dados
        selecionada.votos = F('votos') + 1
        selecionada.save()

    # Redireciona para a página de resultados após o sucesso
    # Isso evita que o usuário vote duas vezes se clicar em "Atualizar" no navegador
    return HttpResponseRedirect(reverse('equetes:resultados', args=(questao.id,)))


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

def nova_alternativa(request, questao_id):
    questao = get_object_or_404(Questao, pk= questao_id)
    if request.method == "POST":
        try:
            form = AlternativaForm(request.POST)
            if form.is_valid():
                alternativa = form.save(commit=False)
                alternativa.questao = questao
                alternativa.save()
        except Exception as e:
            #pode ser tratado ou exibido cosa ocorra algum erro
            form.add_error(None, f"Ocorreu um erro inesperado. {e}")
    return redirect('equetes:detalhes', questao_id=questao.id)