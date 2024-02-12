from django.urls import path
from . import views, json_views

urlpatterns = [
    # Views

    #API Calls
    path("create_category", json_views.create_category, name="create_category"),
    path("create_term", json_views.create_term, name="create_term"),
    path("create_course", json_views.create_course, name="create_course"),
    path("create_lecture", json_views.create_lecture, name="create_lecture"),
    path("create_project", json_views.create_project, name="create_project"),
    path("create_log", json_views.create_log, name="create_log"),
]
