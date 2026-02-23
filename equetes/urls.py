from django.urls import path
from . import views

app_name = "equetes"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:questao_id>/", views.detalhes, name="detalhes"),
    path("<int:questao_id>/voto/", views.voto, name="voto"),
    path("<int:questao_id>/resultados/", views.resultados, name="resultados"),
    path("nova/", views.nova_equete, name="nova_equete"),
    path("<int:questao_id>/nova_alternativa",views.nova_alternativa, name="nova_alternativa"),
    path("alternativa/<int:alternativa_id>/editar/", views.editar_alternativa, name="editar_alternativa"),
    path("alternativa/<int:alternativa_id>/excluir/", views.excluir_alternativa, name="excluir_alternativa"),
]
