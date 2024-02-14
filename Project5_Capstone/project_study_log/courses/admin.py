from django.contrib import admin
from .models import User, Category, Term, Course, Lecture, Project, Log, CourseSection

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Term)
admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Project)
admin.site.register(Log)
