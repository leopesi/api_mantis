from django.urls import path
from .views import ConsultaMantisView

urlpatterns = [
    path('consulta/', ConsultaMantisView.as_view(), name='consulta_mantis'),
]
