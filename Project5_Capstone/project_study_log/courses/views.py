from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import User, Category, Term, Course, Lecture, Project, Log, CourseSection
from datetime import datetime


# ===================================
# SECTION 1: Views
# ===================================
def index(request):
    return render(request, "index.html", {
        'username': request.user.username
    })


def course(request, course_id):
    return render(request, "course.html", {
        'username': request.user.username,
        'course_id': course_id,
        'course_name': Course.objects.get(pk=course_id).name,
        'course_website': Course.objects.get(pk=course_id).website,
    })