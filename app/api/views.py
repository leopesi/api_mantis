import requests
from django.views.generic import FormView, View
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.urls import reverse_lazy
from requests.exceptions import RequestException
import google.generativeai as genai
import os
import logging
from .forms import MantisIssueForm  


logger = logging.getLogger(__name__)

class ConsultaMantisView(FormView):
    template_name = "consulta_mantis.html"  
    form_class = MantisIssueForm  
    success_url = reverse_lazy('mantis_consulta')  # URL de redirecionamento após o sucesso

    def form_valid(self, form):
        issue_id = form.cleaned_data.get('issue_id')
        return self.handle_mantis_issue(self.request, issue_id)

    def handle_mantis_issue(self, request, issue_id):
        return FetchAndAnalyzeMantisIssueView.as_view()(request, issue_id=issue_id)

# Busca os dados do Mantis e faz a análise com o Gemini
class FetchAndAnalyzeMantisIssueView(View):

    def get(self, request, issue_id):
        """Busca os dados da issue no Mantis e analisa com o Gemini."""

        gemini_api_key = os.getenv('API_KEY_GEMINI')
        mantis_auth_token = os.getenv('MANTIS_API_AUTH_TOKEN')

        if not gemini_api_key or not mantis_auth_token:
            return JsonResponse({"error": "Credenciais de API não configuradas."}, status=500)

        genai.configure(api_key=gemini_api_key)
        mantis_api_url = f"https://mantis.xcelis.com.br/mantis/api/rest/issues/{issue_id}"
        api_headers = {'Authorization': mantis_auth_token}

        try:
            # Fazendo a requisição para a API do Mantis
            response = requests.get(mantis_api_url, headers=api_headers)
            response.raise_for_status()  # Levanta exceções se o status não for 200
            logger.debug(f"Resposta da API Mantis: {response}")

            # Verifica se há dados retornados
            issue_data = response.json().get("issues", [])
            if not issue_data:
                return JsonResponse({"error": "Nenhum dado encontrado para a issue."}, status=404)

            issue_data = issue_data[0]

            prompt = (f"Analisar o seguinte problema do Mantis e fornecer um resumo conciso e perspicaz, "
                      f"incluindo um resumo inteligente das atividades: {issue_data}. No Final faça uma sugestão de solução baseado no problema e nas atividades. "
                      f"Colocar negrito quando o texto estiver entre 2 asteriscos, ex.: **Atividades:**")

            try:
                # Geração de conteúdo via Gemini
                model = genai.GenerativeModel('gemini-1.5-flash')
                gemini_response = model.generate_content(prompt)
                gemini_analysis = gemini_response.text
            except Exception as e:
                logger.error(f"Erro ao gerar conteúdo com Gemini: {str(e)}")
                return JsonResponse({"error": "Erro ao gerar conteúdo com o Gemini."}, status=500)

            # Preparar o contexto para renderizar no template
            context = {
                "issue": issue_data,
                "gemini_analysis": gemini_analysis
            }

            # Renderiza o template com os dados da issue e a análise
            return render(request, "mantis_issue.html", context)

        except RequestException as e:
            logger.error(f"Erro ao buscar dados da API Mantis: {str(e)}")
            error_detail = str(e) if settings.DEBUG else "Erro ao buscar ou analisar os dados da issue do Mantis."
            return JsonResponse({"error": error_detail}, status=500)
