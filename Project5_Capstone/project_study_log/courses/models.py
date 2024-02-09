from django.db import models

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'


class Category:
    # Categories allow the user to categorize his courses in major areas
    # Example 1: Intro CS, Core CS, Core Math, CS Tools, Core Systems etc.
    # Example 2: Fundamentals, Technologies, Languages, Interview Prep
    category_name: pass
    category_description: pass


class Term:
    # Terms allow the user to organize his courses by order of completion
    # Example 1: Term 1, Term 2, Term 3, etc.
    # Example 2: Semester 1, Semester 2, Semester 3 etc.
    term_name: pass
    term_start_date: pass
    term_finish_date: pass # term start and finish date are merely informative. They will have no relation to actual dates user started or finished term's courses.


class Course:
    # Courses represent courses (online or not) that should be completed by student
    # Each course must be linked to a category, but linking to a term is optional
    STATUS_OPTIONS = [('N', 'Not started'),('S', 'Started'),('F', 'Finished')]
    course_name: pass
    course_link: pass
    course_hours_forecast: pass # course_hours_forecast is the number of hours that user will forecast for completion of course when creating the course object. It can be compared later to actual number of hours user spent.
    course_status: pass # Course status will inform if course is finished, started or not started.
    # TODO: if I should put number of lectures and number of lectures completed as an attribute or use queries to retrieve it


class Section:
    # Course Content represent sections that need to be completed on a given course.
    STATUS_OPTIONS = [('N', 'Not started'),('S', 'Started'),('F', 'Finished')]
    name: pass
    link: pass
    status: pass # Lecture status will tell if course content is finished, started or not started.    

class Lecture(CourseContent):
    # Lectures represent lectures of a course, but can also represent modules
    # or book chapters, depending on the nature of the course.
    pass

    
class Project:
    # Projects represent projects that user must complete within each course.
    pass

class Log:
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
                 ('RE', 'Review'),
                 ('OT', 'Other'),
                 ('FI', 'Finish')]
    #
    # Attributes
    log_type: pass # Log type should represent the nature of the action user did on given lecture/project
    log_date: pass
    log_content: pass
    log_time: pass
    #
    # Relations
    section: pass

