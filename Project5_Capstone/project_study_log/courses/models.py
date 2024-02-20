from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

NAME_LENGTH = 60
DESCRIPTION_LENGTH = 350
# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)

class User(AbstractUser):
    REQUIRED_FIELDS = []
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    objects = UserManager()
    username = models.CharField(max_length=150, unique=False, null=True, blank=True)


class Category(models.Model):
    """
    Categories allow the user to categorize his courses in major areas
    Example 1: Intro CS, Core CS, Core Math, CS Tools, Core Systems etc.
    Example 2: Fundamentals, Technologies, Languages, Interview Prep
    """
    #
    # Attributes
    name = models.CharField(max_length=NAME_LENGTH)
    description = models.CharField(max_length=DESCRIPTION_LENGTH, null=True, blank=True)
    #
    # Relations
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def serialize(self, user):
        return {
            "id": self.pk,
            "name": self.name,
            "description": self.description,
            "user": self.user.email,
            "total_time_spent": self.total_time_spent,
            "total_courses": self.total_courses,
            "finished_courses": self.finished_courses,
            "hours_forecast": self.hours_forecast,
        }



class Term(models.Model):
    """
    Terms allow the user to organize his courses by order of completion
    Example 1: Term 1, Term 2, Term 3, etc.
    Example 2: Semester 1, Semester 2, Semester 3 etc.
    """
    #
    # Attributes
    name = models.CharField(max_length=NAME_LENGTH)
    start_date = models.DateField(null=True, blank=True)
    finish_date = models.DateField(null=True, blank=True) # term start and finish date are merely informative. They will have no relation to actual dates user started or finished term's courses.
    #
    # Relations
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def serialize(self, user):
        return {
            "id": self.pk,
            "name": self.name,
            "start_date": self.start_date,
            "finish_date": self.finish_date,
            "user": self.user.email,
        }


class Course(models.Model):
    """"
    Courses represent courses (online or not) that should be completed by student
    Each course must be linked to a category, but linking to a term is optional
    """
    #
    # Attributes
    STATUS_CHOICES = [('N', 'Not started'),('S', 'Started'),('F', 'Finished')]
    name = models.CharField(max_length=NAME_LENGTH)
    website = models.URLField(max_length=400, null=True, blank=True)
    hours_forecast = models.PositiveIntegerField(null=True, blank=True) # course_hours_forecast is the number of hours that user will forecast for completion of course when creating the course object. It can be compared later to actual number of hours user spent.
    status = models.CharField(max_length=2, choices=STATUS_CHOICES) # Course status will inform if course is finished, started or not started.
    #
    # Relations
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="course_set")
    term = models.ForeignKey(Term, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.name}"
    
    def serialize(self, user):
        return {
            "id": self.pk,
            "name": self.name,
            "website": self.website,
            "hours_forecast": self.hours_forecast,
            "status": self.status,
            "category": self.category.pk,
            "user": self.category.user.email,
            "total_lectures": self.total_lectures,
            "finished_lectures": self.finished_lectures,
            "total_projects": self.total_projects,
            "finished_projects": self.finished_projects,
            "total_time_spent": self.total_time_spent,
        }

class CourseSection(models.Model):
    """ Course Content represent sections that need to be completed on a given course."""
    STATUS_CHOICES = [('N', 'Not started'),('S', 'Started'),('F', 'Finished')]
    #
    # Attributes
    name = models.CharField(max_length=NAME_LENGTH)
    website = models.URLField(max_length=400, null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES) # Lecture status will tell if course content is finished, started or not started.    
    #
    # Relations
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name = "coursesection_set")

    def __str__(self):
        return f"{self.course.name}: {self.name}"
    
    def serialize(self, user):
        return {
            "id": self.pk,
            "name": self.name,
            "website": self.website,
            "status": self.get_status_display(),
            "course": self.course.pk,
            "category": self.course.category.pk,
            "user": self.course.category.user.email,
            "total_time_spent": self.total_time_spent,
        }


class Lecture(CourseSection):
    """"
    Lectures represent lectures of a course, but can also represent modules
    or book chapters, depending on the nature of the course.
    """
    pass

    
class Project(CourseSection):
    """ Projects represent projects that user must complete within each course."""
    pass

class Log(models.Model):
    """ 
    Logs represent entries on a study journal. They are associated with a Lecture or Project
    They can have varying natures, some examples could be: video viewing session, exercises 
    done, readings done, etc.
    Two special log types should be start and finish. This will indicate that
    user has completed all that he should related to the lecture, and it can be closed.
    """
    LOG_TYPES = [('ST', 'Start'), 
                 ('VS', 'View Session'), 
                 ('EX', 'Exercise'), 
                 ('WS', 'Work Session'),
                 ('RV', 'Review'),
                 ('RD', 'Reading'),
                 ('OT', 'Other'),
                 ('FI', 'Finish')
                 ]
    #
    # Attributes
    type = models.CharField(max_length=2, choices=LOG_TYPES) # Log type should represent the nature of the action user did on given lecture/project
    date = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=DESCRIPTION_LENGTH, null=True, blank=True)
    time_spent = models.PositiveIntegerField(null=True, blank=True)
    #
    # Relations
    course_section = models.ForeignKey(CourseSection, on_delete=models.PROTECT, related_name = 'log_set')

    def __str__(self):
        return f"{self.course_section}: {self.type}, {self.content}"
    
    def serialize(self, user):
        return {
            "id": self.pk,
            "type": self.type,
            "date": self.date,
            "content": self.content,
            "time_spent": self.time_spent,
            "course_section": self.course_section.pk,
            "course": self.course_section.course.pk,
            "category": self.course_section.course.category.pk,
            "user": self.course_section.course.category.user.email,
        }