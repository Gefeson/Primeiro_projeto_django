from django.urls import path
from equetes import views
app_name = "equetes"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:questao_id>/", views.detalhe, name="detalhe"),
    path("<int:questao_id>/voto/", views.voto, name="voto"),
    path("<int:questao_id>/resultado/", views.resultado, name="resultado"),
]
