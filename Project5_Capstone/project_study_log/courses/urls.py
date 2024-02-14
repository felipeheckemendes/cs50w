from django.urls import path
from . import views, json_views

urlpatterns = [
    # Views

    #API Calls
    path("", views.index, name="index"),
    path("create_category", json_views.create_category, name="create_category"),
    path("create_term", json_views.create_term, name="create_term"),
    path("create_course", json_views.create_course, name="create_course"),
    path("create_lecture", json_views.create_lecture, name="create_lecture"),
    path("create_project", json_views.create_project, name="create_project"),
    path("create_log", json_views.create_log, name="create_log"),

    path("get_categories", json_views.get_categories, name="get_categories"),
    path("get_terms", json_views.get_terms, name="get_terms"),

    path("get_courses", json_views.get_courses, name="get_courses"),
    path("get_lectures", json_views.get_lectures, name="get_lectures"),
    path("get_projects", json_views.get_projects, name="get_projects"),
    path("get_logs", json_views.get_logs, name="get_logs"),

    path("delete_object", json_views.delete_object, name="delete_object"),
]
