"""API views for fetching and rendering Mantis issue data."""

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
import json
import os
import requests
from requests.exceptions import HTTPError, RequestException


def mantis_issue_view(request, issue_id):
    """Fetches Mantis issue data by ID and renders it as an HTML table.

    Retrieves API headers from environment variables, makes a request to the Mantis API, 
    and uses a template to render the issue details in a structured table format.

    Args:
        request: The Django request object.
        issue_id: The ID of the Mantis issue to fetch.

    Returns:
        HttpResponse: An HTTP response containing the rendered HTML table if successful, 
                      or a JSON error response if an error occurs.
    """

    try:
        api_headers = json.loads(os.environ["API_HEADERS"])
    except (KeyError, json.JSONDecodeError) as e:
        error_detail = str(e) if settings.DEBUG else "Error retrieving API configuration."
        return JsonResponse({"error": error_detail}, status=500)

    api_url = f"https://mantis.xcelis.com.br/mantis/api/rest/issues/{issue_id}"

    try:
        response = requests.get(api_url, headers=api_headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        issue_data = response.json()["issues"][0]
        template = loader.get_template("mantis_issue_table.html")
        return HttpResponse(template.render({"issue": issue_data}, request))

    except RequestException as e:  # Catch all request-related errors
        error_detail = str(e) if settings.DEBUG else "Error fetching Mantis issue data."
        return JsonResponse({"error": error_detail}, status=500)
