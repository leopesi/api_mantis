"""from django.urls import path
from .views2 import ConsultaMantisView, FetchAndAnalyzeMantisIssueView

urlpatterns = [
    path('consulta/', ConsultaMantisView.as_view(), name='mantis_consulta'),
    path('<str:issue_id>/', FetchAndAnalyzeMantisIssueView.as_view(), name='mantis_issue'),
]
"""
#Funcion Based View
from . import views
from django.urls import path


#Class Based View
from .views2 import ConsultaMantisView, FetchAndAnalyzeMantisIssueView


urlpatterns = [
    #Class Based View
    #path('consulta/', ConsultaMantisView.as_view(), name='mantis_consulta'),
    #path('<int:issue_id>/', FetchAndAnalyzeMantisIssueView.as_view(), name='mantis_issue'),
    
    #Funcion Based View
    path('consulta/', views.consulta_mantis_view, name='consulta_mantis'),
    path("<int:issue_id>/", views.fetch_and_analyze_mantis_issue, name="mantis_issue"),
]
