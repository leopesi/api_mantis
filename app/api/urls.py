from . import views
from django.urls import path

urlpatterns = [
    path('consulta/', views.consulta_mantis_view, name='consulta_mantis'),
    path("<int:issue_id>/", views.mantis_issue_view, name="mantis_issue"),
]