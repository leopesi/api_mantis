import requests
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template import loader
from django.conf import settings
from requests.exceptions import RequestException
import google.generativeai as genai
import os

# Formulário de consulta
def consulta_mantis_view(request):
    if request.method == "POST":
        issue_id = request.POST.get('issue_id')  # Pega o 'issue_id' do POST enviado pelo formulário
        return mantis_issue_view(request, issue_id)
        
    return render(request, "consulta_mantis.html")  # Formulário HTML para realizar a consulta

# Função que realiza a chamada à API do Mantis e análise com Gemini
def mantis_issue_view(request, issue_id):
    """Fetches Mantis issue data, analyzes response with Gemini, and renders it."""

    # Carregar as variáveis de ambiente
    gemini_api_key = os.getenv('API_KEY_GEMINI')
    mantis_auth_token = os.getenv('MANTIS_API_AUTH_TOKEN')

    # Configurar API Gemini com a chave de ambiente
    genai.configure(api_key=gemini_api_key)
    
    api_url = f"https://mantis.xcelis.com.br/mantis/api/rest/issues/{issue_id}"
    api_headers = {'Authorization': mantis_auth_token}

    
    try:
        response = requests.get(api_url, headers=api_headers)
        response.raise_for_status()
        print(response)

        # Obtenha os dados da issue do Mantis
        issue_data = response.json()["issues"][0]

        # Geração de conteúdo via modelo Gemini
        prompt = f"Analisar o seguinte problema do Mantis e fornecer um resumo conciso e perspicaz, incluindo um resumo inteligente das atividades: {issue_data}. No Final faça uma sugestão de solução baseado no problema e nas atividades. colocar negrito quando o texto estiver entre 2asteriscos, ex.: **Atividades:**"
        model = genai.GenerativeModel('gemini-1.5-flash')
        gemini_response = model.generate_content(prompt)

        # Análise de retorno do Gemini
        gemini_analysis = gemini_response.text

        # Renderizar o template com os dados do Mantis e a análise
        template = loader.get_template("mantis_issue.html")
        context = {
            "issue": issue_data,
            "gemini_analysis": gemini_analysis
        }
        return HttpResponse(template.render(context, request))

    except RequestException as e:
        error_detail = str(e) if settings.DEBUG else "Erro ao buscar ou analisar os dados da issue do Mantis."
        return JsonResponse({"error": error_detail}, status=500)

