from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import User, Category, Term, Course, Lecture, Project, Log, CourseSection
from datetime import datetime
from django.apps import apps
from django.db.models import ProtectedError, Count, Sum, Q



# ===================================
# SECTION 1: API views for creating elements
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
    return JsonResponse({"message": f"{NAME_FOR_MESSAGES} {name} created with success.", "id": category.id}, status=201)


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
    return JsonResponse({"message": f"{NAME_FOR_MESSAGES} {name} created with success.", "id": term.id}, status=201)
    

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
    return JsonResponse({"message": f"{NAME_FOR_MESSAGES} {name} created with success.", "id": course.id}, status=201)


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
    return JsonResponse({"message": f"{NAME_FOR_MESSAGES} {name} created with success.", "id": lecture.id}, status=201)


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
    return JsonResponse({"message": f"{NAME_FOR_MESSAGES} {name} created with success.", "id": project.id}, status=201)


def create_log(request):
    """
    Add an entry to database for a new log
    Parameters: request
    Side effects: creates a new log inside the database. (Accepts multiple logs with same name.)
    Returns: JsonResponse with:
        - A status code depending on the success of database addition.
        - A message telling if the log was successfully created or not, and the reason why not.
    """
    print("FUNCTION CREATE LOG STARTED")
    NAME_FOR_MESSAGES = "Log"
    # ERROR HANDLING 1: If method is not POST, return 400 with error message
    if request.method != "POST":
        print("ERROR 0")
        return JsonResponse({"message": "POST request required."}, status=400)
    
    # ERROR HANDLING 2: Check if user is not logged in
    if not request.user.is_authenticated:
        print("ERROR 1")
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} creation failed: you must log in before creating a new {NAME_FOR_MESSAGES}."}, status=400)
    
    # ERROR HANDLING 3: Try to convert the POST body to a python dictionary
    try:
        data = json.loads(request.body)
    except:
        print("ERROR 2")
        return JsonResponse({"message": "Invalid or empty JSON."}, status=400)
    
    # ERROR HANDLING 4: Check if type is not None
    if data.get("type") not in ['ST', 'VS', 'EX', 'WS', 'RV', 'RD', 'OT', 'FI']:
        print("ERROR 3")
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not created. Type must not be one of the options on the list."}, status=400)
        
    # ERROR HANDLING 5: Check if there was provided a course_section_id of an existing course_section to which attach the course.
    if not CourseSection.objects.filter(pk=data.get("course_section_id")).exists():
        print("ERROR 4")
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not created. Lecture or Project does not exist on the database or not provided."}, status=400)
    
    # ERROR HANDLING 6: Check if lecture/project to which the course will be attached belongs to current user.
    if not CourseSection.objects.get(pk=data.get("course_section_id")).course.category.user == request.user:
        print("ERROR 5")
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not created. Lecture or Project does not belong to current user."}, status=400)

    # ERRO HANDLING 7: Check if time spent is positive integer
    if data.get("time_spent") != None:
        print(data)
        if not isinstance(int(data.get("time_spent")), int) or int(data.get("time_spent")) < 0:
            print("ERROR 6")
            return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not created. {NAME_FOR_MESSAGES}'s forecasted duration must be a whole number."}, status=400)

    # Add new log to database and return 201.
    type = data.get("type")
    content = data.get("content")
    time_spent = int(data.get("time_spent"))
    course_section_id = data.get("course_section_id")
    log = Log(type=type, 
              content=content, 
              time_spent=time_spent,
              course_section=CourseSection.objects.get(pk=course_section_id), 
              )
    log.save()
    print("ERROR 7")
    return JsonResponse({"message": f"{NAME_FOR_MESSAGES} created with success.", "id": log.id}, status=201)


# ===================================
# SECTION 2: API views for getting elements
# ===================================

def get_categories(request):
    """
    Get the category list for current user and pass to front-end
    Parameters: request
    Side effects: None
    Returns: JsonResponse with:
        - A status code depending on the success of database query.
        - A message telling if search retrieved any categories or not
        - A list of the categories, with name and id, and other relevant information
    """
    NAME_FOR_MESSAGES = "Categories"
    # ERROR HANDLING 1: Check if user is signed in
    if not request.user.is_authenticated:
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not retrieved. You must log in first."}, status=401)

    # ERROR HANDLING 2: Check if request method is GET
    if request.method != "GET":
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not retrieved. GET request required."}, status=405)

    # ERROR HANDLING 3: Check if there is any categories associated with user, return empty list
    categories = Category.objects.select_related('user').filter(user=request.user)
    categories = categories.annotate(total_time_spent=Sum('course_set__coursesection_set__log_set__time_spent')/60)
    categories = categories.annotate(total_courses=Count('course_set'))
    categories = categories.annotate(finished_courses=Count('course_set', filter=Q(course_set__status='F')))
    categories = categories.annotate(hours_forecast=Sum('course_set__hours_forecast'))
    if not categories.exists():
        return JsonResponse({'results': {},
                             'message': f"{NAME_FOR_MESSAGES} not retrieved. User has not created any categories yet."})

    categories = categories.order_by('name')
    data = {
        'results': [category.serialize(request.user) for category in categories],
        'message': f"{NAME_FOR_MESSAGES} retrieved successfully."
    }

    return JsonResponse(data, safe=False)


def get_terms(request):
    """
    Get the term list for current user and pass to front-end
    Parameters: request
    Side effects: None
    Returns: JsonResponse with:
        - A status code depending on the success of database query.
        - A message telling if search retrieved any terms or not
        - A list of the terms, with name and id, and other relevant information
    """
    NAME_FOR_MESSAGES = "Terms"
    print("========================================")
    # ERROR HANDLING 1: Check if user is signed in
    if not request.user.is_authenticated:
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not retrieved. You must log in first."}, status=401)

    # ERROR HANDLING 2: Check if request method is GET
    if request.method != "GET":
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not retrieved. GET request required."}, status=405)

    # ERROR HANDLING 3: Check if there is any terms associated with user, return empty list
    terms = Term.objects.select_related('user').filter(user=request.user)
    if not terms.exists():
        return JsonResponse({'results': {},
                             'message': f"{NAME_FOR_MESSAGES} not retrieved. User has not created any terms yet."})

    terms = terms.order_by('name')
    data = {
        'results': [term.serialize(request.user) for term in terms],
        'message': f"{NAME_FOR_MESSAGES} retrieved successfully."
    }

    return JsonResponse(data, safe=False)


def get_courses(request):
    """
    Get the course list for current user and pass to front-end
    Parameters: request
    Side effects: None
    Returns: JsonResponse with:
        - A status code depending on the success of database query.
        - A message telling if search retrieved any courses or not
        - A list of the courses, with name and id, and other relevant information
    """
    NAME_FOR_MESSAGES = "Courses"
    # ERROR HANDLING 1: Check if user is signed in
    if not request.user.is_authenticated:
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not retrieved. You must log in first."}, status=401)

    # ERROR HANDLING 2: Check if request method is GET
    if request.method != "GET":
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not retrieved. GET request required."}, status=405)

    # ERROR HANDLING 3: Check if there is any courses associated with user
    courses = Course.objects.select_related('category__user').filter(category__user=request.user)
    courses = courses.annotate(total_lectures=Count('coursesection_set__lecture'))
    courses = courses.annotate(finished_lectures=Count('coursesection_set__lecture', filter=Q(coursesection_set__status='F')))
    courses = courses.annotate(total_projects=Count('coursesection_set__project'))
    courses = courses.annotate(finished_projects=Count('coursesection_set__project', filter=Q(coursesection_set__status='F')))
    courses = courses.annotate(total_time_spent=Sum('coursesection_set__log_set__time_spent')/60)
    if not courses.exists():
        return JsonResponse({'results': {},
                             "message": f"{NAME_FOR_MESSAGES} not retrieved. User has not created any courses yet."})

    courses = courses.order_by('name')
    data = {
        'results': [course.serialize(request.user) for course in courses],
        'message': f"{NAME_FOR_MESSAGES} retrieved successfully."
    }

    return JsonResponse(data, safe=False)


def get_lectures(request):
    """
    Get the lecture list for current user and pass to front-end
    Parameters: request
    Side effects: None
    Returns: JsonResponse with:
        - A status code depending on the success of database query.
        - A message telling if search retrieved any lectures or not
        - A list of the lectures, with name and id, and other relevant information
    """
    NAME_FOR_MESSAGES = "Lectures"
    # ERROR HANDLING 1: Check if user is signed in
    if not request.user.is_authenticated:
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not retrieved. You must log in first."}, status=401)

    # ERROR HANDLING 2: Check if request method is GET
    if request.method != "GET":
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not retrieved. GET request required."}, status=405)

    # ERROR HANDLING 3: Check if there is any data associated with user
    lectures = Lecture.objects.select_related('course__category__user').filter(course__category__user=request.user)
    lectures = lectures.annotate(total_time_spent=Sum('log_set__time_spent')/60)
    if not lectures.exists():
        return JsonResponse({'results': {},
                             "message": f"{NAME_FOR_MESSAGES} not retrieved. User has not created any lectures yet."})

    lectures = lectures.order_by('name')
    data = {
        'results': [lecture.serialize(request.user) for lecture in lectures],
        'message': f"{NAME_FOR_MESSAGES} retrieved successfully."
    }

    return JsonResponse(data, safe=False)


def get_projects(request):
    """
    Get the project list for current user and pass to front-end
    Parameters: request
    Side effects: None
    Returns: JsonResponse with:
        - A status code depending on the success of database query.
        - A message telling if search retrieved any projects or not
        - A list of the projects, with name and id, and other relevant information
    """
    NAME_FOR_MESSAGES = "Projects"
    # ERROR HANDLING 1: Check if user is signed in
    if not request.user.is_authenticated:
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not retrieved. You must log in first."}, status=401)

    # ERROR HANDLING 2: Check if request method is GET
    if request.method != "GET":
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not retrieved. GET request required."}, status=405)

    # ERROR HANDLING 3: Check if there is any data associated with user
    projects = Project.objects.select_related('course__category__user').filter(course__category__user=request.user)
    projects = projects.annotate(total_time_spent=Sum('log_set__time_spent')/60)
    if not projects.exists():
        return JsonResponse({'results': {},
                             "message": f"{NAME_FOR_MESSAGES} not retrieved. User has not created any projects yet."})

    projects = projects.order_by('name')
    data = {
        'results': [project.serialize(request.user) for project in projects],
        'message': f"{NAME_FOR_MESSAGES} retrieved successfully."
    }

    return JsonResponse(data, safe=False)


def get_logs(request):
    """
    Get the log list for current user and pass to front-end
    Parameters: request
    Side effects: None
    Returns: JsonResponse with:
        - A status code depending on the success of database query.
        - A message telling if search retrieved any logs or not
        - A list of the logs, with name and id, and other relevant information
    """
    NAME_FOR_MESSAGES = "Logs"
    # ERROR HANDLING 1: Check if user is signed in
    if not request.user.is_authenticated:
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not retrieved. You must log in first."}, status=401)

    # ERROR HANDLING 2: Check if request method is GET
    if request.method != "GET":
        return JsonResponse({"message": f"{NAME_FOR_MESSAGES} not retrieved. GET request required."}, status=405)

    # ERROR HANDLING 3: Check if there is any data associated with user
    logs = Log.objects.select_related('course_section__course__category__user').filter(course_section__course__category__user=request.user)
    if not logs.exists():
        return JsonResponse({'results': {},
                             "message": f"{NAME_FOR_MESSAGES} not retrieved. User has not created any logs yet."})

    logs = logs.order_by('date')
    data = {
        'results': [log.serialize(request.user) for log in logs],
        'message': f"{NAME_FOR_MESSAGES} retrieved successfully."
    }

    return JsonResponse(data, safe=False)


# ===================================
# SECTION 3: API views for deleting elements
# ===================================
def delete_object(request):
    """
    Delete a chosen category.
    Parameters: request. ID will be on request.POST
    Side effects: Category is deleted from the database
    Returns: JsonResponse with:
        - A status code depending on the success of database deletion.
        - A message telling if object was deleted or if there was some issue and which.
    """
    request.POST.get('object_model')
    request.POST.get('id')

    # ERROR HANDLING 1: Check if user is signed in
    if not request.user.is_authenticated:
        return JsonResponse({"message": f"Not possible to delete. You must log in first."}, status=401)

    # ERROR HANDLING 2: Check if request method is POST
    if request.method != "POST":
        return JsonResponse({"message": f"Not possible to delete. POST request required."}, status=405)

    # ERROR HANDLING 3: Check if object to delete exists
    data = json.loads(request.body)
    object_model = data.get('object_model')
    object_id = data.get('id')

    Model = apps.get_model('courses', object_model)
    object_exists = Model.objects.filter(id=object_id).exists()
    if not object_exists:
        return JsonResponse({"message": f"Not possible to delete. Object not retrieved."}, status=404)

    # ERROR HANDLING 4: Check if the object is owned by the user making the request
    relation_strings = {
        'Category': {'user': request.user},
        'Course': {'category__user': request.user},
        'Lecture': {'course__category__user': request.user},
        'Project': {'course__category__user': request.user},
        'Log': {'course_section__course__category__user': request.user}
    }
    is_object_owned_by_user = Model.objects.filter(**relation_strings[object_model]).exists()

    if not is_object_owned_by_user:
        return JsonResponse({"message": f"Not possible to delete. Object is not owned by current user."}, status=403)

    # Try to delete. If not possible, raise errors
    object = Model.objects.get(pk=object_id)
    try:
        object.delete()
        return JsonResponse({"message": f"Object deleted."})
    except ProtectedError:
        return JsonResponse({"message": f"Not possible to delete. Please delete all child objects before deleting object."}, status=409)
    except Exception as e:
        return JsonResponse({"message": f"Not possible to delete. {e}."}, status=400)

    



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