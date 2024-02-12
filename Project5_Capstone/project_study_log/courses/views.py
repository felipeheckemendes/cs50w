from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import User, Category, Term, Course, Lecture, Project, Log, CourseSection
from datetime import datetime


# ===================================
# SECTION 1: Views
# ===================================
