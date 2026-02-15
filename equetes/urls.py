from django.urls import path
from . import views

app_name = "equetes"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:questao_id>/", views.detalhes, name="detalhes"),
    path("<int:questao_id>/voto/", views.voto, name="voto"),
    path("<int:questao_id>/resultados/", views.resultados, name="resultados"),
    path("nova/", views.nova_enquete, name="nova_enquete"),
    path("<int:questao.id>/nova_alternativa",views.nova_alternativa, name="nova_alternativa")
]
