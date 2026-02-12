from django.urls import path
from . import views

app_name = "equetes"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:questao_id>/", views.detalhes, name="detalhes"),
    path("<int:questao_id>/voto/", views.voto, name="voto"),
    path("<int:questao_id>/resultados/", views.resultados, name="resultados"),
]
