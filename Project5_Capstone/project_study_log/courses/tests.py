from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import User, Category, Term, Course, Lecture, Project, Log, CourseSection

# CATEGORY tests
class CategoryTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(email='testuser@email.com', password='123456qwe')
    
    def test_create_category_succesful(self):
        self.client.login(email='testuser@email.com', password='123456qwe')

            
        # CASE SUCCESS 1: Test if a category was created succesfully
        test_category_name = "Category 1"
        test_category_description = "This is Category 1s description."
        response = self.client.post("/create_category", {'name': test_category_name, 'description': test_category_description}, content_type='application/json')
        #with open('error_page.html', 'wb') as f:
        #    f.write(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'], f"Category {test_category_name} created with success.")
        self.assertTrue(Category.objects.filter(user=self.test_user, name=test_category_name, description =test_category_description).exists())

        # CASE SUCCESS 2: Test if a category without description was created succesfully
        test_category_name = "Category 2"
        test_category_description = ""
        response = self.client.post("/create_category", {'name': test_category_name, 'description': test_category_description}, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'], f"Category {test_category_name} created with success.")
        self.assertTrue(Category.objects.filter(user=self.test_user, name=test_category_name, description =test_category_description).exists())

    def test_create_category_unsuccesful(self):
        self.client.login(email='testuser@email.com', password='123456qwe')

        # CASE FAIL 1: blank string for category name
        test_category_name = ""
        test_category_description = "This is Category 1s description."
        response = self.client.post("/create_category", {'name': test_category_name, 'description': test_category_description}, content_type='application/json')
        self.assertEqual(response.status_code, 400, "CASE FAIL 1: Code was not 400 when expected")
        self.assertEqual(response.json()['message'], f"Category not created. Name must not be blank.", "CASE FAIL 1: Message returned was not the expected one")
        self.assertFalse(Category.objects.filter(user=self.test_user, name=test_category_name, description =test_category_description).exists(), "CASE FAIL 1: New category was found within the database when was expected not to be")

        # CASE FAIL 2: " " string for category name
        test_category_name = " "
        test_category_description = "This is Category 1s description."
        response = self.client.post("/create_category", {'name': test_category_name, 'description': test_category_description}, content_type='application/json')
        self.assertEqual(response.status_code, 400, "CASE FAIL 2: Code was not 400 when expected")
        self.assertEqual(response.json()['message'], f"Category not created. Name must not be blank.", "CASE FAIL 2: Message returned was not the expected one")
        self.assertFalse(Category.objects.filter(user=self.test_user, name=test_category_name, description =test_category_description).exists(), "CASE FAIL 2: New category was found within the database when was expected not to be")

        # CASE FAIL 3: None for category name
        test_category_name = None
        test_category_description = "This is Category 1s description."
        response = self.client.post("/create_category", {'name': test_category_name, 'description': test_category_description}, content_type='application/json')
        self.assertEqual(response.status_code, 400, "CASE FAIL 3: Code was not 400 when expected")
        self.assertEqual(response.json()['message'], f"Category not created. Name must not be blank.", "CASE FAIL 3: Message returned was not the expected one")
        self.assertFalse(Category.objects.filter(user=self.test_user, name=test_category_name, description =test_category_description).exists(), "CASE FAIL 3: New category was found within the database when was expected not to be")

        # CASE FAIL 4: method was not post
        test_category_name = "Category 1"
        test_category_description = "This is Category 1s description."
        response = self.client.get("/create_category", {'name': test_category_name, 'description': test_category_description}, content_type='application/json')
        self.assertEqual(response.status_code, 400, "CASE FAIL 4: Code was not 400 when expected")
        self.assertEqual(response.json()['message'], f"POST request required.", "CASE FAIL 4: Message returned was not the expected one")
        self.assertFalse(Category.objects.filter(name=test_category_name, description =test_category_description).exists(), "CASE FAIL 4: New category was found within the database when was expected not to be")

        # CASE FAIL 5: User was not logged in
        self.client.logout()
        test_category_name = "Category 1"
        test_category_description = "This is Category 1s description."
        response = self.client.post("/create_category", {'name': test_category_name, 'description': test_category_description}, content_type='application/json')
        self.assertEqual(response.status_code, 400, "CASE FAIL 5: Code was not 400 when expected")
        self.assertEqual(response.json()['message'], f"Category creation failed: you must log in before creating a new category.", "CASE FAIL 5: Message returned was not the expected one")
        self.assertFalse(Category.objects.filter(name=test_category_name, description =test_category_description).exists(), "CASE FAIL 5: New category was found within the database when was expected not to be")

# TERM test
class TermTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(email='testuser@email.com', password='123456qwe')
    
    def test_create_term_succesful(self):
        self.client.login(email='testuser@email.com', password='123456qwe')

            
        # CASE SUCCESS 1: Test if a term was created succesfully
        test_term_name = "Term 1"
        start_date = '2024-01-21'
        finish_date = '2024-06-21'
        post_data = {'name': test_term_name, 'start_date': start_date, 'finish_date': finish_date}
        response = self.client.post("/create_term", post_data, content_type='application/json')
        #with open('error_page.html', 'wb') as f:
        #    f.write(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'], f"Term {test_term_name} created with success.")
        self.assertTrue(Term.objects.filter(user=self.test_user, 
                                            name=test_term_name, 
                                            start_date=start_date, 
                                            finish_date=finish_date
                                            ).exists())

        # CASE SUCCESS 2: Test if a term without datas was created succesfully
        test_term_name = "Term 2"
        start_date = ''
        finish_date = None
        post_data = {'name': test_term_name, 'start_date': start_date, 'finish_date': finish_date}
        response = self.client.post("/create_term", post_data, content_type='application/json')
        #with open('error_page.html', 'wb') as f:
        #    f.write(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'], f"Term {test_term_name} created with success.")
        self.assertTrue(Term.objects.filter(user=self.test_user, 
                                            name=test_term_name,
                                            ).exists())

    def test_create_term_unsuccesful(self):
        self.client.login(email='testuser@email.com', password='123456qwe')

        # CASE FAIL 1: blank string for term name
        test_term_name = ""
        start_date = '2024-01-21'
        finish_date = '2024-06-21'
        post_data = {'name': test_term_name, 'start_date': start_date, 'finish_date': finish_date}
        response = self.client.post("/create_term", post_data, content_type='application/json')
        self.assertEqual(response.status_code, 400, "CASE FAIL 1: Code was not 400 when expected")
        self.assertEqual(response.json()['message'], f"Term not created. Name must not be blank.", "CASE FAIL 1: Message returned was not the expected one")
        self.assertFalse(Term.objects.filter(user=self.test_user, 
                                             name=test_term_name, 
                                             ).exists(), "CASE FAIL 1: New term was found within the database when was expected not to be")

        # CASE FAIL 2: " " string for term name
        test_term_name = " "
        start_date = '2024-01-21'
        finish_date = '2024-06-21'
        post_data = {'name': test_term_name, 'start_date': start_date, 'finish_date': finish_date}
        response = self.client.post("/create_term", post_data, content_type='application/json')
        self.assertEqual(response.status_code, 400, "CASE FAIL 1: Code was not 400 when expected")
        self.assertEqual(response.json()['message'], f"Term not created. Name must not be blank.", "CASE FAIL 1: Message returned was not the expected one")
        self.assertFalse(Term.objects.filter(user=self.test_user, 
                                             name=test_term_name, 
                                             ).exists(), "CASE FAIL 2: New term was found within the database when was expected not to be")

        # CASE FAIL 3: None for term name
        test_term_name = None
        start_date = '2024-01-21'
        finish_date = '2024-06-21'
        post_data = {'name': test_term_name, 'start_date': start_date, 'finish_date': finish_date}
        response = self.client.post("/create_term", post_data, content_type='application/json')
        self.assertEqual(response.status_code, 400, "CASE FAIL 1: Code was not 400 when expected")
        self.assertEqual(response.json()['message'], f"Term not created. Name must not be blank.", "CASE FAIL 1: Message returned was not the expected one")
        self.assertFalse(Term.objects.filter(user=self.test_user, 
                                             name=test_term_name, 
                                             ).exists(), "CASE FAIL 3: New term was found within the database when was expected not to be")

        # CASE FAIL 4: method was not post
        test_term_name = "Term 1"
        start_date = '2024-01-21'
        finish_date = '2024-06-21'
        post_data = {'name': test_term_name, 'start_date': start_date, 'finish_date': finish_date}
        response = self.client.get("/create_term", post_data, content_type='application/json')
        #with open('error_page.html', 'wb') as f:
        #    f.write(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], f"POST request required.", "CASE FAIL 4: Message returned was not the expected one")
        self.assertFalse(Term.objects.filter(user=self.test_user, 
                                             name=test_term_name, 
                                             ).exists(), "CASE FAIL 4: New term was found within the database when was expected not to be")
      
        # CASE FAIL 5: User was not logged in
        self.client.logout()
        test_term_name = "Term 1"
        start_date = '2024-01-21'
        finish_date = '2024-06-21'
        post_data = {'name': test_term_name, 'start_date': start_date, 'finish_date': finish_date}
        response = self.client.post("/create_term", post_data, content_type='application/json')
        #with open('error_page.html', 'wb') as f:
        #    f.write(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], f"Term creation failed: you must log in before creating a new term.", "CASE FAIL 5: Message returned was not the expected one")
        self.assertFalse(Term.objects.filter(user=self.test_user, 
                                             name=test_term_name, 
                                             ).exists(), "CASE FAIL 5: New term was found within the database when was expected not to be")
        

# COURSE TEST
class CourseTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(email='testuser@email.com', password='123456qwe')
    
    def test_create_course_succesful(self):
        self.client.login(email='testuser@email.com', password='123456qwe')

        # CASE SUCCESS 1: Test if a course was created succesfully
        test_category_name = "Category 1"
        test_category_description = "This is Category 1s description."
        response = self.client.post("/create_category", {'name': test_category_name, 'description': test_category_description}, content_type='application/json')

        test_course_name = "Course 1"
        website = 'www.mit.com'
        hours_forecast = 10
        category_id = 1
        post_data = {'name': test_course_name, 
                     'website': website, 
                     'hours_forecast': hours_forecast,
                     'category_id': category_id,
                     }
        response = self.client.post("/create_course", post_data, content_type='application/json')
        #with open('error_page.html', 'wb') as f:
        #    f.write(response.content)
        self.assertEqual(response.json()['message'], f"Course {test_course_name} created with success.")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Course.objects.filter(name=test_course_name, 
                                              website=website, 
                                              category=Category.objects.get(pk=category_id)
                                              ).exists())
        
        # CASE SUCCESS 2: Test if a course can be created without a hours_forecast and without website.
        test_category_name = "Category 1"
        test_category_description = "This is Category 1s description."
        response = self.client.post("/create_category", {'name': test_category_name, 'description': test_category_description}, content_type='application/json')

        test_course_name = "Course 1"
        website = None
        hours_forecast = None
        category_id = 1
        post_data = {'name': test_course_name, 
                     'website': website, 
                     'hours_forecast': hours_forecast,
                     'category_id': category_id,
                     }
        response = self.client.post("/create_course", post_data, content_type='application/json')
        #with open('error_page.html', 'wb') as f:
        #    f.write(response.content)
        self.assertEqual(response.json()['message'], f"Course {test_course_name} created with success.")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Course.objects.filter(name=test_course_name, 
                                              website=website, 
                                              category=Category.objects.get(pk=category_id)
                                              ).exists())
        

    def test_create_course_unsuccesful(self):
        self.client.login(email='testuser@email.com', password='123456qwe')

        # CASE FAIL 1: Test that a course CANNOT be created without a category, and returns appropriate message.
        test_category_name = "Category 1"
        test_category_description = "This is Category 1s description."
        response = self.client.post("/create_category", {'name': test_category_name, 'description': test_category_description}, content_type='application/json')

        test_course_name = "Course 1"
        website = None
        hours_forecast = None
        category_id = None
        post_data = {'name': test_course_name, 
                     'website': website, 
                     'hours_forecast': hours_forecast,
                     'category_id': category_id,
                     }
        response = self.client.post("/create_course", post_data, content_type='application/json')
        #with open('error_page.html', 'wb') as f:
        #    f.write(response.content)
        self.assertEqual(response.json()['message'], f"Course not created. Category does not exist on the database or not provided.")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Course.objects.filter(name=test_course_name, 
                                              website=website,
                                              ).exists())
        
        # CASE FAIL 2: Test that a course CANNOT be created without a name, and returns appropriate message.
        test_category_name = "Category 1"
        test_category_description = "This is Category 1s description."
        response = self.client.post("/create_category", {'name': test_category_name, 'description': test_category_description}, content_type='application/json')

        test_course_name = ""
        website = None
        hours_forecast = None
        category_id = 1
        post_data = {'name': test_course_name, 
                     'website': website, 
                     'hours_forecast': hours_forecast,
                     'category_id': category_id,
                     }
        response = self.client.post("/create_course", post_data, content_type='application/json')
        #with open('error_page.html', 'wb') as f:
        #    f.write(response.content)
        self.assertEqual(response.json()['message'], f"Course not created. Name must not be blank.")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Course.objects.filter(name=test_course_name, 
                                              website=website,
                                              ).exists())
        
        # CASE FAIL 3: Method was not POST
        test_category_name = "Category 1"
        test_category_description = "This is Category 1s description."
        response = self.client.post("/create_category", {'name': test_category_name, 'description': test_category_description}, content_type='application/json')

        test_course_name = "Course 1"
        website = "www.mit.com"
        hours_forecast = 10
        category_id = 1
        post_data = {'name': test_course_name, 
                     'website': website, 
                     'hours_forecast': hours_forecast,
                     'category_id': category_id,
                     }
        response = self.client.get("/create_course", post_data, content_type='application/json')
        #with open('error_page.html', 'wb') as f:
        #    f.write(response.content)
        self.assertEqual(response.json()['message'], f"POST request required.")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Course.objects.filter(name=test_course_name, 
                                              website=website,
                                              ).exists())
        
        # CASE FAIL 4: User was not logged in.
        self.client.logout()
        test_category_name = "Category 1"
        test_category_description = "This is Category 1s description."
        response = self.client.post("/create_category", {'name': test_category_name, 'description': test_category_description}, content_type='application/json')

        test_course_name = "Course 1"
        website = None
        hours_forecast = 10
        category_id = 1
        post_data = {'name': test_course_name, 
                     'website': website, 
                     'hours_forecast': hours_forecast,
                     'category_id': category_id,
                     }
        response = self.client.post("/create_course", post_data, content_type='application/json')
        #with open('error_page.html', 'wb') as f:
        #    f.write(response.content)
        self.assertEqual(response.json()['message'], f"Course creation failed: you must log in before creating a new Course.")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Course.objects.filter(name=test_course_name, 
                                              website=website,
                                              ).exists())
        

        # CASE FAIL 4: Trying to attach course to a category that does not belong to user.
        test_category_name = "Category 1"
        test_category_description = "This is Category 1s description."
        response = self.client.post("/create_category", {'name': test_category_name, 'description': test_category_description}, content_type='application/json')
        self.client.logout()
        self.test_user2 = User.objects.create_user(email='felipe@gmail.com', password='123456qwe')
        self.client.login(email='felipe@gmail.com', password='123456qwe'),

        test_course_name = "Course 1"
        website = None
        hours_forecast = 10
        category_id = 1
        post_data = {'name': test_course_name, 
                     'website': website, 
                     'hours_forecast': hours_forecast,
                     'category_id': category_id,
                     }
        response = self.client.post("/create_course", post_data, content_type='application/json')
        #with open('error_page.html', 'wb') as f:
        #    f.write(response.content)
        self.assertEqual(response.json()['message'], f"Course not created. Category does not belong to current user.")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Course.objects.filter(name=test_course_name, 
                                              website=website,
                                              ).exists())

#LECTURE test
class LectureTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(email='testuser@email.com', password='123456qwe')
    
    def test_create_lecture_succesful(self):
        self.client.login(email='testuser@email.com', password='123456qwe')

        # CASE SUCCESS 1: Test if a lecture was created succesfully
        # Create a category
        test_category_name = "Category 1"
        test_category_description = "This is Category 1s description."
        response = self.client.post("/create_category", {'name': test_category_name, 'description': test_category_description}, content_type='application/json')

        # Create a course
        test_course_name = "Course 1"
        website = 'www.mit.com'
        hours_forecast = 10
        category_id = 1
        post_data = {'name': test_course_name, 
                     'website': website, 
                     'hours_forecast': hours_forecast,
                     'category_id': category_id,
                     }
        response = self.client.post("/create_course", post_data, content_type='application/json')

        # CASE SUCCESS 1: Create a normal Lecture
        test_lecture_name = "Lecture 1"
        test_lecture_website = "www.mit.com/lecture1"
        course_id = 1
        post_data = {'name': test_lecture_name, 
                     'website': test_lecture_website, 
                     'course_id': course_id,
                     }
        response = self.client.post("/create_lecture", post_data, content_type='application/json')

        self.assertEqual(response.json()['message'], f"Lecture {test_lecture_name} created with success.")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Lecture.objects.filter(name=test_lecture_name, 
                                              website=test_lecture_website, 
                                              course=Course.objects.get(pk=course_id)
                                              ).exists())
        
        # CASE SUCCESS 2: Create a Lecture without website
        test_lecture_name = "Lecture 1"
        test_lecture_website = None
        course_id = 1
        post_data = {'name': test_lecture_name, 
                     'website': test_lecture_website, 
                     'course_id': course_id,
                     }
        response = self.client.post("/create_lecture", post_data, content_type='application/json')

        self.assertEqual(response.json()['message'], f"Lecture {test_lecture_name} created with success.")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Lecture.objects.filter(name=test_lecture_name, 
                                              website=test_lecture_website, 
                                              course=Course.objects.get(pk=course_id)
                                              ).exists())
        
    def test_create_lecture_fail(self):
        self.client.login(email='testuser@email.com', password='123456qwe')

        # Create a category
        test_category_name = "Category 1"
        test_category_description = "This is Category 1s description."
        response = self.client.post("/create_category", {'name': test_category_name, 'description': test_category_description}, content_type='application/json')

        # Create a course
        test_course_name = "Course 1"
        website = 'www.mit.com'
        hours_forecast = 10
        category_id = 1
        post_data = {'name': test_course_name, 
                     'website': website, 
                     'hours_forecast': hours_forecast,
                     'category_id': category_id,
                     }
        response = self.client.post("/create_course", post_data, content_type='application/json')

        # CASE FAIL 1: Mothod is not POST
        test_lecture_name = "Lecture 1"
        test_lecture_website = ""
        course_id = 1
        post_data = {'name': test_lecture_name, 
                     'website': test_lecture_website, 
                     'course_id': course_id,
                     }
        response = self.client.get("/create_lecture", post_data, content_type='application/json')

        self.assertEqual(response.json()['message'], f"POST request required.")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Lecture.objects.filter(name=test_lecture_name, 
                                              course=Course.objects.get(pk=course_id)
                                              ).exists())
        
        # CASE FAIL 2: Lecture without name
        test_lecture_name = ""
        test_lecture_website = None
        course_id = 1
        post_data = {'name': test_lecture_name, 
                     'website': test_lecture_website, 
                     'course_id': course_id,
                     }
        response = self.client.post("/create_lecture", post_data, content_type='application/json')

        self.assertEqual(response.json()['message'], f"Lecture not created. Name must not be blank.")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Lecture.objects.filter(name=test_lecture_name, 
                                              course=Course.objects.get(pk=course_id)
                                              ).exists())
        
        # CASE FAIL 3: Lecture without course attached
        test_lecture_name = "Lecture 3"
        test_lecture_website = None
        course_id = None
        post_data = {'name': test_lecture_name, 
                     'website': test_lecture_website, 
                     'course_id': course_id,
                     }
        response = self.client.post("/create_lecture", post_data, content_type='application/json')

        self.assertEqual(response.json()['message'], f"Lecture not created. Course does not exist on the database or not provided.")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Lecture.objects.filter(name=test_lecture_name, 
                                              ).exists())
        

        # CASE FAIL 4: Attached course belongs to another user
        test_lecture_name = "Lecture 1"
        test_lecture_website = None
        course_id = 1
        post_data = {'name': test_lecture_name, 
                     'website': test_lecture_website, 
                     'course_id': course_id,
                     }
        
        self.client.logout()
        self.test_user2 = User.objects.create_user(email='felipe@gmail.com', password='123456qwe')
        self.client.login(email='felipe@gmail.com', password='123456qwe'),

        response = self.client.post("/create_lecture", post_data, content_type='application/json')
        
        self.assertEqual(response.json()['message'], f"Lecture not created. Course category does not belong to current user.")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Lecture.objects.filter(name=test_lecture_name, 
                                              course=Course.objects.get(pk=course_id)
                                              ).exists())
        

        # CASE FAIL 5: User not logged in
        test_lecture_name = "Lecture 1"
        test_lecture_website = None
        course_id = 1
        post_data = {'name': test_lecture_name, 
                     'website': test_lecture_website, 
                     'course_id': course_id,
                     }
        
        self.client.logout()

        response = self.client.post("/create_lecture", post_data, content_type='application/json')
        
        self.assertEqual(response.json()['message'], f"Lecture creation failed: you must log in before creating a new Lecture.")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Lecture.objects.filter(name=test_lecture_name, 
                                              course=Course.objects.get(pk=course_id)
                                              ).exists())
        
#PROJECT test
class ProjectTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(email='testuser@email.com', password='123456qwe')
    
    def test_create_project_succesful(self):
        self.client.login(email='testuser@email.com', password='123456qwe')

        # CASE SUCCESS 1: Test if a project was created succesfully
        # Create a category
        test_category_name = "Category 1"
        test_category_description = "This is Category 1s description."
        response = self.client.post("/create_category", {'name': test_category_name, 'description': test_category_description}, content_type='application/json')

        # Create a course
        test_course_name = "Course 1"
        website = 'www.mit.com'
        hours_forecast = 10
        category_id = 1
        post_data = {'name': test_course_name, 
                     'website': website, 
                     'hours_forecast': hours_forecast,
                     'category_id': category_id,
                     }
        response = self.client.post("/create_course", post_data, content_type='application/json')

        # CASE SUCCESS 1: Create a normal Project
        test_project_name = "Project 1"
        test_project_website = "www.mit.com/project1"
        course_id = 1
        post_data = {'name': test_project_name, 
                     'website': test_project_website, 
                     'course_id': course_id,
                     }
        response = self.client.post("/create_project", post_data, content_type='application/json')

        self.assertEqual(response.json()['message'], f"Project {test_project_name} created with success.")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Project.objects.filter(name=test_project_name, 
                                              website=test_project_website, 
                                              course=Course.objects.get(pk=course_id)
                                              ).exists())
        
        # CASE SUCCESS 2: Create a Project without website
        test_project_name = "Project 1"
        test_project_website = None
        course_id = 1
        post_data = {'name': test_project_name, 
                     'website': test_project_website, 
                     'course_id': course_id,
                     }
        response = self.client.post("/create_project", post_data, content_type='application/json')

        self.assertEqual(response.json()['message'], f"Project {test_project_name} created with success.")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Project.objects.filter(name=test_project_name, 
                                              website=test_project_website, 
                                              course=Course.objects.get(pk=course_id)
                                              ).exists())
        
    def test_create_project_fail(self):
        self.client.login(email='testuser@email.com', password='123456qwe')

        # Create a category
        test_category_name = "Category 1"
        test_category_description = "This is Category 1s description."
        response = self.client.post("/create_category", {'name': test_category_name, 'description': test_category_description}, content_type='application/json')

        # Create a course
        test_course_name = "Course 1"
        website = 'www.mit.com'
        hours_forecast = 10
        category_id = 1
        post_data = {'name': test_course_name, 
                     'website': website, 
                     'hours_forecast': hours_forecast,
                     'category_id': category_id,
                     }
        response = self.client.post("/create_course", post_data, content_type='application/json')

        # CASE FAIL 1: Mothod is not POST
        test_project_name = "Project 1"
        test_project_website = ""
        course_id = 1
        post_data = {'name': test_project_name, 
                     'website': test_project_website, 
                     'course_id': course_id,
                     }
        response = self.client.get("/create_project", post_data, content_type='application/json')

        self.assertEqual(response.json()['message'], f"POST request required.")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Project.objects.filter(name=test_project_name, 
                                              course=Course.objects.get(pk=course_id)
                                              ).exists())
        
        # CASE FAIL 2: Project without name
        test_project_name = ""
        test_project_website = None
        course_id = 1
        post_data = {'name': test_project_name, 
                     'website': test_project_website, 
                     'course_id': course_id,
                     }
        response = self.client.post("/create_project", post_data, content_type='application/json')

        self.assertEqual(response.json()['message'], f"Project not created. Name must not be blank.")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Project.objects.filter(name=test_project_name, 
                                              course=Course.objects.get(pk=course_id)
                                              ).exists())
        
        # CASE FAIL 3: Project without course attached
        test_project_name = "Project 3"
        test_project_website = None
        course_id = None
        post_data = {'name': test_project_name, 
                     'website': test_project_website, 
                     'course_id': course_id,
                     }
        response = self.client.post("/create_project", post_data, content_type='application/json')

        self.assertEqual(response.json()['message'], f"Project not created. Course does not exist on the database or not provided.")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Project.objects.filter(name=test_project_name, 
                                              ).exists())
        

        # CASE FAIL 4: Attached course belongs to another user
        test_project_name = "Project 1"
        test_project_website = None
        course_id = 1
        post_data = {'name': test_project_name, 
                     'website': test_project_website, 
                     'course_id': course_id,
                     }
        
        self.client.logout()
        self.test_user2 = User.objects.create_user(email='felipe@gmail.com', password='123456qwe')
        self.client.login(email='felipe@gmail.com', password='123456qwe'),

        response = self.client.post("/create_project", post_data, content_type='application/json')
        
        self.assertEqual(response.json()['message'], f"Project not created. Course category does not belong to current user.")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Project.objects.filter(name=test_project_name, 
                                              course=Course.objects.get(pk=course_id)
                                              ).exists())
        

        # CASE FAIL 5: User not logged in
        test_project_name = "Project 1"
        test_project_website = None
        course_id = 1
        post_data = {'name': test_project_name, 
                     'website': test_project_website, 
                     'course_id': course_id,
                     }
        
        self.client.logout()

        response = self.client.post("/create_project", post_data, content_type='application/json')
        
        self.assertEqual(response.json()['message'], f"Project creation failed: you must log in before creating a new Project.")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Project.objects.filter(name=test_project_name, 
                                              course=Course.objects.get(pk=course_id)
                                              ).exists())
        

#LOG test
class LogTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(email='testuser@email.com', password='123456qwe')
    
    def test_create_log_succesful(self):
        self.client.login(email='testuser@email.com', password='123456qwe')

        # CASE SUCCESS 1: Test if a log was created succesfully
        # Create a Category
        test_category_name = "Category 1"
        test_category_description = "This is Category 1s description."
        response = self.client.post("/create_category", {'name': test_category_name, 'description': test_category_description}, content_type='application/json')

        # Create a Course
        test_course_name = "Course 1"
        website = 'www.mit.com'
        hours_forecast = 10
        category_id = 1
        post_data = {'name': test_course_name, 
                     'website': website, 
                     'hours_forecast': hours_forecast,
                     'category_id': category_id,
                     }
        response = self.client.post("/create_course", post_data, content_type='application/json')

        # Create a Project
        test_project_name = "Project 1"
        test_project_website = "www.mit.com/project1"
        course_id = 1
        post_data = {'name': test_project_name, 
                     'website': test_project_website, 
                     'course_id': course_id,
                     }
        response = self.client.post("/create_project", post_data, content_type='application/json')

        # CASE SUCESS 1: Create a basic log on the database
        test_log_type = "ST"
        test_log_content = "This is my log's content"
        test_log_time_spent = 90
        course_section_id = 1

        post_data = {'type': test_log_type, 
                     'content': test_log_content,
                     'time_spent': test_log_time_spent,
                     'course_section_id': course_section_id
                     }
        response = self.client.post("/create_log", post_data, content_type='application/json')

        self.assertEqual(response.json()['message'], f"Log created with success.")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Log.objects.filter(type=test_log_type,
                                           content=test_log_content,
                                           time_spent=test_log_time_spent,
                                           course_section=CourseSection.objects.get(pk=course_section_id)).exists())
        
        # CASE SUCESS 2: Create a log without time_spent and without content
        test_log_type = "ST"
        test_log_content = None
        test_log_time_spent = None
        course_section_id = 1

        post_data = {'type': test_log_type, 
                     'content': test_log_content,
                     'time_spent': test_log_time_spent,
                     'course_section_id': course_section_id
                     }
        response = self.client.post("/create_log", post_data, content_type='application/json')

        self.assertEqual(response.json()['message'], f"Log created with success.")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Log.objects.filter(type=test_log_type,
                                           content=test_log_content,
                                           course_section=CourseSection.objects.get(pk=course_section_id)).exists())
        

    def test_create_log_fail(self):
        self.client.login(email='testuser@email.com', password='123456qwe')

        # Create a Category
        test_category_name = "Category 1"
        test_category_description = "This is Category 1s description."
        response = self.client.post("/create_category", {'name': test_category_name, 'description': test_category_description}, content_type='application/json')

        # Create a Course
        test_course_name = "Course 1"
        website = 'www.mit.com'
        hours_forecast = 10
        category_id = 1
        post_data = {'name': test_course_name, 
                     'website': website, 
                     'hours_forecast': hours_forecast,
                     'category_id': category_id,
                     }
        response = self.client.post("/create_course", post_data, content_type='application/json')

        # Create a Project
        test_project_name = "Project 1"
        test_project_website = "www.mit.com/project1"
        course_id = 1
        post_data = {'name': test_project_name, 
                     'website': test_project_website, 
                     'course_id': course_id,
                     }
        response = self.client.post("/create_project", post_data, content_type='application/json')

        # CASE FAIL 1: Create a basic log without a type
        test_log_type = None
        test_log_content = "This is my log's content"
        test_log_time_spent = 90
        course_section_id = 1

        post_data = {'type': test_log_type, 
                     'content': test_log_content,
                     'time_spent': test_log_time_spent,
                     'course_section_id': course_section_id
                     }
        response = self.client.post("/create_log", post_data, content_type='application/json')

        self.assertEqual(response.json()['message'], f"Log not created. Type must not be one of the options on the list.")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Log.objects.filter(content=test_log_content,
                                           time_spent=test_log_time_spent,
                                           course_section=CourseSection.objects.get(pk=course_section_id)).exists())
        
        # CASE FAIL 2: Create a basic log with type not on the list
        test_log_type = "SS"
        test_log_content = "This is my log's content"
        test_log_time_spent = 90
        course_section_id = 1

        post_data = {'type': test_log_type, 
                     'content': test_log_content,
                     'time_spent': test_log_time_spent,
                     'course_section_id': course_section_id
                     }
        response = self.client.post("/create_log", post_data, content_type='application/json')

        self.assertEqual(response.json()['message'], f"Log not created. Type must not be one of the options on the list.")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Log.objects.filter(type=test_log_type,
                                           content=test_log_content,
                                           time_spent=test_log_time_spent,
                                           course_section=CourseSection.objects.get(pk=course_section_id)).exists())
        
        # CASE FAIL 3: Create a basic log without course_section attached
        test_log_type = "ST"
        test_log_content = "This is my log's content"
        test_log_time_spent = 90
        course_section_id = None

        post_data = {'type': test_log_type, 
                     'content': test_log_content,
                     'time_spent': test_log_time_spent,
                     'course_section_id': course_section_id
                     }
        response = self.client.post("/create_log", post_data, content_type='application/json')

        self.assertEqual(response.json()['message'], f"Log not created. Lecture or Project does not exist on the database or not provided.")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Log.objects.filter(type=test_log_type,
                                           content=test_log_content,
                                           time_spent=test_log_time_spent
                                           ).exists())
        
        # CASE FAIL 4: Create a log with id of a course section that does not exist 
        test_log_type = "ST"
        test_log_content = "This is my log's content DIFFERENTIATE"
        test_log_time_spent = 90
        course_section_id = 1500

        post_data = {'type': test_log_type, 
                     'content': test_log_content,
                     'time_spent': test_log_time_spent,
                     'course_section_id': course_section_id
                     }
        response = self.client.post("/create_log", post_data, content_type='application/json')

        self.assertEqual(response.json()['message'], f"Log not created. Lecture or Project does not exist on the database or not provided.")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Log.objects.filter(content=test_log_content,
                                           time_spent=test_log_time_spent,
                                           ).exists())       

        # CASE FAIL 5: Create a log with id of a course that belongs to another user 
        test_log_type = "ST"
        test_log_content = "This is my log's content"
        test_log_time_spent = 90
        course_section_id = 1

        self.client.logout()
        self.test_user2 = User.objects.create_user(email='felipe@gmail.com', password='123456qwe')
        self.client.login(email='felipe@gmail.com', password='123456qwe'),

        post_data = {'type': test_log_type, 
                     'content': test_log_content,
                     'time_spent': test_log_time_spent,
                     'course_section_id': course_section_id
                     }
        response = self.client.post("/create_log", post_data, content_type='application/json')

        self.assertEqual(response.json()['message'], f"Log not created. Lecture or Project does not belong to current user.")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Log.objects.filter(content=test_log_content,
                                           time_spent=test_log_time_spent,
                                           course_section=CourseSection.objects.get(pk=course_section_id)).exists())
        

        # CASE FAIL 6: Create a log while logged out 
        test_log_type = "ST"
        test_log_content = "This is my log's content"
        test_log_time_spent = 90
        course_section_id = 1

        self.client.logout()

        post_data = {'type': test_log_type, 
                     'content': test_log_content,
                     'time_spent': test_log_time_spent,
                     'course_section_id': course_section_id
                     }
        response = self.client.post("/create_log", post_data, content_type='application/json')

        self.assertEqual(response.json()['message'], f"Log creation failed: you must log in before creating a new Log.")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Log.objects.filter(content=test_log_content,
                                           time_spent=test_log_time_spent,
                                           course_section=CourseSection.objects.get(pk=course_section_id)).exists())    
        

        # CASE FAIL 7: Method is not POST
        test_log_type = "ST"
        test_log_content = "This is my log's content"
        test_log_time_spent = 90
        course_section_id = 1

        self.client.logout()

        post_data = {'type': test_log_type, 
                     'content': test_log_content,
                     'time_spent': test_log_time_spent,
                     'course_section_id': course_section_id
                     }
        response = self.client.get("/create_log", post_data, content_type='application/json')

        self.assertEqual(response.json()['message'], f"POST request required.")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Log.objects.filter(content=test_log_content,
                                           time_spent=test_log_time_spent,
                                           course_section=CourseSection.objects.get(pk=course_section_id)).exists())    