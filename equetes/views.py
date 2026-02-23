
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.db.models import F
from django.urls import reverse
from .models import Questao, Alternativa, Voto
from .forms import QuestaoForm, AlternativaForm
from django.contrib.auth.decorators import login_required


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

@login_required
def voto(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    #Verifica se o User já votou nesta questão
    ja_votou = Voto.objects.filter(usuario=request.user, questao=questao).exists()
    if ja_votou:
        contexto= {'questao': questao, 'error_message': "Você já participou desta enquete.", }
        return render(request, 'equetes/detalhes.html', contexto)
    
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
    #   selecionada.votos = F('votos') + 1
    #   selecionada.save()
        Voto.objects.create(usuario=request.user, questao=questao, alternativa=selecionada) #Cria e salva objeto voto no Banco de dados
    # Redireciona para a página de resultados após o sucesso
    # Isso evita que o usuário vote duas vezes se clicar em "Atualizar" no navegador
    return HttpResponseRedirect(reverse('equetes:resultados', args=(questao.id,)))


def resultados(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'equetes/resultados.html', {'questao':questao})

@login_required
def nova_equete(request):
    if request.method == "POST":
        try:
            form = QuestaoForm(request.POST)
            if form.is_valid():
                # salva questao mas não envia ao banco ainda (commit=False)
                # para podermos definir a data de publicação via código
                questao = form.save(commit=False)
                questao.criador = request.user
                questao.data_pub = timezone.now()
                questao.save()
                return redirect('equetes:index')
        except Exception as e:
            form.add_error(None,f"Ocorreu um erro inesperado. {e}")
    else:
        form = QuestaoForm()
        
    return render(request, 'equetes/cadastro.html', {'form': form})

@login_required
def nova_alternativa(request, questao_id):
    questao = get_object_or_404(Questao, pk= questao_id)  
    if questao.usuario != request.user:
        return HttpResponseForbidden()  
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

@login_required
def excluir_alternativa(request, alternativa_id):
    alternativa = get_object_or_404(Alternativa, pk=alternativa_id)
    questao_id = alternativa.questao.id
    
    if request.method == "POST":
        alternativa.delete()
    
    return redirect('equetes:detalhes', questao_id)


@login_required
def editar_alternativa(request, alternativa_id):
    alternativa = get_object_or_404(Alternativa, pk=alternativa_id)
    questao = alternativa.questao
    
    if request.method == "POST":
        '''o argumento 'instance' é o segrede: ele is ao django para
        atualizar o objeto existente em vez de criar um novo'''
        form_alternativa = AlternativaForm(request.POST, instance=alternativa)
        if form_alternativa.is_valid():
            form_alternativa.save()
            return redirect('equetes:detalhes', questao_id=questao.id)
    else:
        #GET: carrega os formulário preenchido comos dados atuais
        form_alternativa = AlternativaForm(instance=alternativa)
    contexto = {'form_alternativa': form_alternativa, 'alternativa': alternativa}
    return render(request, 'equetes/editar_alternativa.html', contexto)
        
        
    
