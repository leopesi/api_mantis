from . import views
from django.urls import path
urlpatterns = [
    path("<int:issue_id>/", views.mantis_issue_view, name="mantis_issue"),
]