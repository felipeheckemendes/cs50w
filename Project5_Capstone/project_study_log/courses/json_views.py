from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import User, Category, Term, Course, Lecture, Project, Log, CourseSection
from datetime import datetime


# ===================================
# SECTION 1: API views
# ===================================
def create_category(request):
    """
    Add an entry to database for a new category
    Parameters: request
    Side effects: creates a new category inside the database. (Accepts multiple categories with same name.)
    Returns: JsonResponse with:
        - A status code depending on the success of database addition.
        - A message telling if the category was successfully created or not, and the reason why not.
    """
    NAME_FOR_MESSAGES = "Category"
    # ERROR HANDLING 1: If method is not POST, return 400 with error message
    if request.method != "POST":
        return JsonResponse({"message": "POST request required."}, status=400)
    
    # ERROR HANDLING 2: Try to convert the POST body to a python dictionary
    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"message": "Invalid or empty JSON."}, status=400)

    # ERROR HANDLING 3: Check if name is not None
    name = data.get("name")
    description = data.get("description")
    if not name or not name.strip():
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not created. Name must not be blank."}, status=400)
    
    # ERROR HANDLING 4: Check if user is not logged in
    if not request.user.is_authenticated:
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} creation failed: you must log in before creating a new category."}, status=400)

    # Add new category to database and return 201.
    category = Category(name=name, description=description, user=request.user)
    category.save()
    return JsonResponse({"message": f"{NAME_FOR_MESSAGES} {name} created with success."}, status=201)


def create_term(request):
    """
    Add an entry to database for a new term
    Parameters: request
    Side effects: creates a new term inside the database. (Accepts multiple terms with same name.)
    Returns: JsonResponse with:
        - A status code depending on the success of database addition.
        - A message telling if the term was successfully created or not, and the reason why not.
    """
    NAME_FOR_MESSAGES = "Term"
    # ERROR HANDLING 1: If method is not POST, return 400 with error message
    if request.method != "POST":
        return JsonResponse({"message": "POST request required."}, status=400)
    
    # ERROR HANDLING 2: Try to convert the POST body to a python dictionary
    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"message": "Invalid or empty JSON."}, status=400)

    # ERROR HANDLING 3: Check if name is not None
    name = data.get("name")
    start_date = str_to_date(data.get("start_date"), "%Y-%m-%d")
    finish_date = str_to_date(data.get("finish_date"), "%Y-%m-%d")
    if not name or not name.strip():
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not created. Name must not be blank."}, status=400)
    
    # ERROR HANDLING 4: Check if user is not logged in
    if not request.user.is_authenticated:
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} creation failed: you must log in before creating a new term."}, status=400)

    # Add new term to database and return 201.
    term = Term(name=name, start_date=start_date, finish_date=finish_date, user=request.user)
    term.save()
    return JsonResponse({"message": f"{NAME_FOR_MESSAGES} {name} created with success."}, status=201)
    

def create_course(request):
    """
    Add an entry to database for a new course
    Parameters: request
    Side effects: creates a new course inside the database. (Accepts multiple courses with same name.)
    Returns: JsonResponse with:
        - A status code depending on the success of database addition.
        - A message telling if the course was successfully created or not, and the reason why not.
    """
    NAME_FOR_MESSAGES = "Course"
    # ERROR HANDLING 1: If method is not POST, return 400 with error message
    if request.method != "POST":
        return JsonResponse({"message": "POST request required."}, status=400)
    
    # ERROR HANDLING 2: Check if user is not logged in
    if not request.user.is_authenticated:
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} creation failed: you must log in before creating a new {NAME_FOR_MESSAGES}."}, status=400)
    
    # ERROR HANDLING 3: Try to convert the POST body to a python dictionary
    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"message": "Invalid or empty JSON."}, status=400)
    
    # ERROR HANDLING 4: Check if name is not None
    if not data.get("name") or not data.get("name").strip():
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not created. Name must not be blank."}, status=400)
    
    # ERROR HANDLING 5: Check if hours_forecast is integer
    if data.get("hours_forecast") != None:
        if not isinstance(data.get("hours_forecast"), int) or data.get("hours_forecast") < 0:
            return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not created. {NAME_FOR_MESSAGES}'s forecasted duration must be a whole number."}, status=400)
        
    # ERROR HANDLING 5: Check if there was provided a category_id of an existing category to which attach the course.
    if not Category.objects.filter(pk=data.get("category_id")).exists():
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not created. Category does not exist on the database or not provided."}, status=400)
    
    # ERROR HANDLING 6: Check if category to which the course will be attached belongs to current user.
    if not Category.objects.get(pk=data.get("category_id")).user == request.user:
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not created. Category does not belong to current user."}, status=400)

    # Add new course to database and return 201.
    name = data.get("name")
    website = data.get("website")
    hours_forecast = data.get("hours_forecast")
    status = 'N'
    category_id = data.get("category_id")
    course = Course(name=name, 
                website=website, 
                hours_forecast=hours_forecast, 
                status=status, 
                category=Category.objects.get(pk=category_id), 
                )
    course.save()
    return JsonResponse({"message": f"{NAME_FOR_MESSAGES} {name} created with success."}, status=201)


def create_lecture(request):
    """
    Add an entry to database for a new lecture
    Parameters: request
    Side effects: creates a new lecture inside the database. (Accepts multiple courses with same name.)
    Returns: JsonResponse with:
        - A status code depending on the success of database addition.
        - A message telling if the lecture was successfully created or not, and the reason why not.
    """
    NAME_FOR_MESSAGES = "Lecture"
    # ERROR HANDLING 1: If method is not POST, return 400 with error message
    if request.method != "POST":
        return JsonResponse({"message": "POST request required."}, status=400)
    
    # ERROR HANDLING 2: Check if user is not logged in
    if not request.user.is_authenticated:
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} creation failed: you must log in before creating a new {NAME_FOR_MESSAGES}."}, status=400)
    
    # ERROR HANDLING 3: Try to convert the POST body to a python dictionary
    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"message": "Invalid or empty JSON."}, status=400)
    
    # ERROR HANDLING 4: Check if name is not None
    if not data.get("name") or not data.get("name").strip():
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not created. Name must not be blank."}, status=400)
        
    # ERROR HANDLING 5: Check if there was provided a course_id of an existing course to which attach the course.
    if not Course.objects.filter(pk=data.get("course_id")).exists():
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not created. Course does not exist on the database or not provided."}, status=400)
    
    # ERROR HANDLING 6: Check if category to which the course will be attached belongs to current user.
    if not Course.objects.get(pk=data.get("course_id")).category.user == request.user:
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not created. Course category does not belong to current user."}, status=400)

    # Add new lecture to database and return 201.
    name = data.get("name")
    website = data.get("website")
    status = 'N'
    course_id = data.get("course_id")
    lecture = Lecture(name=name, 
                website=website, 
                status=status,
                course=Course.objects.get(pk=course_id), 
                )
    lecture.save()
    return JsonResponse({"message": f"{NAME_FOR_MESSAGES} {name} created with success."}, status=201)


def create_project(request):
    """
    Add an entry to database for a new project
    Parameters: request
    Side effects: creates a new project inside the database. (Accepts multiple courses with same name.)
    Returns: JsonResponse with:
        - A status code depending on the success of database addition.
        - A message telling if the project was successfully created or not, and the reason why not.
    """
    NAME_FOR_MESSAGES = "Project"
    # ERROR HANDLING 1: If method is not POST, return 400 with error message
    if request.method != "POST":
        return JsonResponse({"message": "POST request required."}, status=400)
    
    # ERROR HANDLING 2: Check if user is not logged in
    if not request.user.is_authenticated:
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} creation failed: you must log in before creating a new {NAME_FOR_MESSAGES}."}, status=400)
    
    # ERROR HANDLING 3: Try to convert the POST body to a python dictionary
    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"message": "Invalid or empty JSON."}, status=400)
    
    # ERROR HANDLING 4: Check if name is not None
    if not data.get("name") or not data.get("name").strip():
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not created. Name must not be blank."}, status=400)
        
    # ERROR HANDLING 5: Check if there was provided a course_id of an existing course to which attach the course.
    if not Course.objects.filter(pk=data.get("course_id")).exists():
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not created. Course does not exist on the database or not provided."}, status=400)
    
    # ERROR HANDLING 6: Check if category to which the course will be attached belongs to current user.
    if not Course.objects.get(pk=data.get("course_id")).category.user == request.user:
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not created. Course category does not belong to current user."}, status=400)

    # Add new project to database and return 201.
    name = data.get("name")
    website = data.get("website")
    status = 'N'
    course_id = data.get("course_id")
    project = Project(name=name, 
                website=website, 
                status=status,
                course=Course.objects.get(pk=course_id), 
                )
    project.save()
    return JsonResponse({"message": f"{NAME_FOR_MESSAGES} {name} created with success."}, status=201)


def create_log(request):
    """
    Add an entry to database for a new log
    Parameters: request
    Side effects: creates a new log inside the database. (Accepts multiple logs with same name.)
    Returns: JsonResponse with:
        - A status code depending on the success of database addition.
        - A message telling if the log was successfully created or not, and the reason why not.
    """
    NAME_FOR_MESSAGES = "Log"
    # ERROR HANDLING 1: If method is not POST, return 400 with error message
    if request.method != "POST":
        return JsonResponse({"message": "POST request required."}, status=400)
    
    # ERROR HANDLING 2: Check if user is not logged in
    if not request.user.is_authenticated:
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} creation failed: you must log in before creating a new {NAME_FOR_MESSAGES}."}, status=400)
    
    # ERROR HANDLING 3: Try to convert the POST body to a python dictionary
    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"message": "Invalid or empty JSON."}, status=400)
    
    # ERROR HANDLING 4: Check if type is not None
    if data.get("type") not in ['ST', 'VS', 'EX', 'WS', 'RV', 'RD', 'OT', 'FI']:
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not created. Type must not be one of the options on the list."}, status=400)
        
    # ERROR HANDLING 5: Check if there was provided a course_section_id of an existing course_section to which attach the course.
    if not CourseSection.objects.filter(pk=data.get("course_section_id")).exists():
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not created. Lecture or Project does not exist on the database or not provided."}, status=400)
    
    # ERROR HANDLING 6: Check if lecture/project to which the course will be attached belongs to current user.
    if not CourseSection.objects.get(pk=data.get("course_section_id")).course.category.user == request.user:
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not created. Lecture or Project does not belong to current user."}, status=400)

    # ERRO HANDLING 7: Check if time spent is positive integer
    if data.get("time_spent") != None:
        if not isinstance(data.get("time_spent"), int) or data.get("time_spent") < 0:
            return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not created. {NAME_FOR_MESSAGES}'s forecasted duration must be a whole number."}, status=400)

    # Add new log to database and return 201.
    type = data.get("type")
    content = data.get("content")
    time_spent = data.get("time_spent")
    course_section_id = data.get("course_section_id")
    log = Log(type=type, 
              content=content, 
              time_spent=time_spent,
              course_section=CourseSection.objects.get(pk=course_section_id), 
              )
    log.save()
    return JsonResponse({"message": f"{NAME_FOR_MESSAGES} created with success."}, status=201)

# ===================================
# SECTION X: Utilities
# ===================================
def str_to_date(date_string, date_format):
    if date_string == None:
        return None
    try:
        return datetime.strptime(date_string, date_format)
    except ValueError:
        return None