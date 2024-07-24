from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests # type: ignore
from django.template import loader
import os
import json
from django.conf import settings
from requests.exceptions import HTTPError, RequestException
# ... your other views ...pip

def mantis_issue_view(request, issue_id):
    """Fetches Mantis issue data, dynamically renders an HTML table."""
    try:
        # Fetch API headers from environment
        api_headers_str = os.environ.get("API_HEADERS")
        if not api_headers_str:
            raise ValueError("API_HEADERS environment variable not found")

        api_headers = json.loads(api_headers_str)
    except (json.JSONDecodeError, ValueError) as e:
        if settings.DEBUG:
            error_detail = str(e)  # Include detailed error in debug mode
        else:
            error_detail = "Error parsing or retrieving API headers"
        return JsonResponse({"error": error_detail}, status=500)

    api_url = f"https://mantis.xcelis.com.br/mantis/api/rest/issues/{issue_id}"

    try:
        response = requests.get(api_url, headers=api_headers)
        response.raise_for_status()  # Raise exception for bad HTTP status codes

        issue_data = response.json()["issues"][0]

        template = loader.get_template("mantis_issue_table.html")
        context = {"issue": issue_data}
        return HttpResponse(template.render(context, request))

    except (HTTPError, RequestException) as e:
        if settings.DEBUG:
            error_detail = str(e)
        else:
            error_detail = "Error fetching Mantis issue data"
        return JsonResponse({"error": error_detail}, status=500)
