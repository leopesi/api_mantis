from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests # type: ignore
from django.template import loader

# ... your other views ...

def mantis_issue_view(request, issue_id):
    """Fetches Mantis issue data, dynamically renders an HTML table."""

    api_url = "https://mantis.xcelis.com.br/mantis/api/rest/issues/{}"
    api_headers = {'Authorization': 'KEY'}

    url = api_url.format(issue_id)

    try:
        response = requests.get(url, headers=api_headers)
        response.raise_for_status()

        data = response.json()
        issue = data["issues"][0]  

        template = loader.get_template("mantis_issue_table.html")
        context = {"issue": issue}  # Pass the entire issue dictionary to the template
        return HttpResponse(template.render(context, request))

    except requests.exceptions.RequestException as e:
        error_message = {"error": "Failed to fetch Mantis issue data.", "details": str(e)}
        return JsonResponse(error_message, status=500)