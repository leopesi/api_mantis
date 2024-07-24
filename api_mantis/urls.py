from . import views
from django.urls import path

urlpatterns = [
    #path('home', views.index, name='about'),
    path("issue/<int:issue_id>/", views.mantis_issue_view, name="mantis_issue"),

    ]
# path('post/list/', views.PostListView.as_view(), name='post_list'),