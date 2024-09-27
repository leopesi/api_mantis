import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.conf import settings
from requests.exceptions import RequestException
import google.generativeai as genai
import os
import logging

from .forms import ConsultaMantisForm

logger = logging.getLogger(__name__)

class ConsultaMantisView(View):
    template_name = "consulta_mantis.html"
    form_class = ConsultaMantisForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            issue_id = form.cleaned_data.get('issue_id')
            return self.fetch_and_analyze_mantis_issue(request, issue_id)
        return render(request, self.template_name, {"form": form}, status=400)

    def fetch_and_analyze_mantis_issue(self, request, issue_id):
        gemini_api_key = os.getenv('API_KEY_GEMINI')
        mantis_auth_token = os.getenv('MANTIS_API_AUTH_TOKEN')

        if not gemini_api_key or not mantis_auth_token:
            logger.error("API credentials are missing. Check API_KEY_GEMINI and MANTIS_API_AUTH_TOKEN environment variables.")
            return JsonResponse({"error": "API credentials are not configured correctly."}, status=500)

        genai.configure(api_key=gemini_api_key)
        mantis_api_url = f"https://mantis.xcelis.com.br/mantis/api/rest/issues/{issue_id}"
        api_headers = {'Authorization': mantis_auth_token}

        try:
            response = requests.get(mantis_api_url, headers=api_headers, timeout=10)
            response.raise_for_status()
            logger.debug(f"API Response for issue {issue_id}: {response.status_code} - {response.text}")

            issue_data = response.json().get("issues", [])
            if not isinstance(issue_data, list) or not issue_data:
                logger.error(f"No valid issue data returned for issue_id {issue_id}")
                return JsonResponse({"error": "Nenhum dado encontrado para a issue."}, status=404)
            issue_data = issue_data[0]

            prompt = (f"Analisar o chamado {issue_data} e fornecer um resumo conciso e perspicaz"
                      f"Destaque os campos ID, Solicitante, Date Submitted, Last Update, Assigned To, Summary"
                      f"Reproduza o campo Description"
                      f"Faça um resumo inteligente, para leigos em TI, das Activities: {issue_data} com as datas de cada atualização. Instruções: #INICIOATENDIMENTO indica o início do atendimento, #COMUNICACAO indica que o Solicitante foi comunicado, #SOLUCAO indica que o problema foi resolvido"
                      f"Faça uma conclusão resumida das do campo Activities em ordem cronológica"
                      f"Escreva tudo em português"
                      )

            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                gemini_response = model.generate_content(prompt)
                gemini_analysis = gemini_response.text
            except Exception as e:
                logger.error(f"Erro ao gerar conteúdo com Gemini: {str(e)}")
                if settings.DEBUG:
                    return JsonResponse({"error": f"Erro ao gerar conteúdo com o Gemini: {str(e)}"}, status=500)
                return JsonResponse({"error": "Erro ao gerar conteúdo com o Gemini."}, status=500)

            context = {
                "issue": issue_data,
                "gemini_analysis": gemini_analysis
            }
            return render(request, "mantis_issue.html", context)

        except requests.Timeout:
            logger.error(f"Timeout occurred while trying to fetch issue {issue_id}")
            return JsonResponse({"error": "Timeout occurred while fetching issue."}, status=500)
        except RequestException as e:
            logger.error(f"Erro ao buscar dados da API Mantis: {str(e)}")
            error_detail = str(e) if settings.DEBUG else "Erro ao buscar ou analisar os dados da issue do Mantis."
            return JsonResponse({"error": error_detail}, status=500)
