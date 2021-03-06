from django.test import TestCase
from App import App
from UserEdits import UserEdits
from CourseEdit import CourseEdit
from Login import Login
from Final.DjangoInterface import DjangoInterface
from Final.models import User
from Final.models import Course
from django.test.client import RequestFactory
from django.test import Client
from django.test.utils import setup_test_environment


class TestApp(TestCase):

    def setUp(self):
        # Setting up mock database
        self.test_user = User.objects.create(username="testUsername", password="testPassword", permissions="1111",
                                             address="testAddress", phonenumber="TestPhoneNum", email="TestEmail")
        User.objects.create(username="brokenUsername", password="brokenPassword", permissions="0000",
                            address="testAddress", phonenumber="TestPhoneNum", email="TestEmail")
        User.objects.create(username="delUsername", password="delPassword", permissions="0000",
                            address="testAddress", phonenumber="TestPhoneNum", email="TestEmail")
        Course.objects.create(instructor="testInstructor", courseId="testCourse",
                              startTime="1pm", endTime="2pm")
        User.objects.create(username="TAUsername", password="testPassword", permissions="0001",
                            address="testAddress", phonenumber="TestPhoneNum", email="TestEmail")

        self.client = Client()
        self.client1 = Client()
        session = self.client1.session
        session['user'] = 'username'
        session.save()
        self.factory = RequestFactory()

    def test_login_page_is_accessible(self):
        response = self.client.get('/loginpage/')
        self.assertEqual(response.status_code, 200)

    def test_login_page_user_is_successful(self):
        response = self.client1.get('/loginpage/')
        self.assertRedirects(response, '/landingpage/')

    def test_login_fails_render_login_template(self):
        r = self.client.post('/loginpage/', data={'username': 'test', 'password': 'test'})
        self.assertTemplateUsed(r, 'main/loginpage.html')

    def test_login_passes_render_landing_page(self):
        r = self.client.post('/loginpage/', data={'username': 'testUsername', 'password': 'testPassword'})
        self.assertRedirects(r, '/landingpage/')

    def test_login_wrongusername_unsucessful(self):
        response = self.client.post('/loginpage/', data={'username': 'u', 'password': 'p'})
        str = 'User does not exist'
        self.assertEqual(response.context['loginResponse'], str)

    def test_login_wrongpassword_unsucessful(self):
        response = self.client.post('/loginpage/', data={'username': 'testUsername', 'password': 'p'})
        str = 'Username or password is incorrect'
        self.assertEqual(response.context['loginResponse'], str)

    def test_logout_successful_redirect(self):
        response = self.client.post('/logout/')
        self.assertRedirects(response, '/loginpage/')

    def test_login_to_database(self):
        a = App(Login(DjangoInterface()), UserEdits(), CourseEdit())
        # assume username is in the directory/database
        result1 = a.command("login BadUser testPassword")
        result2 = a.command("login testUsername BadPass")
        result3 = a.command("login testUsername testPassword")
        # Error cases
        self.assertEqual("User does not exist", result1)  # Username will trip this failure first.
        self.assertEqual("Incorrect username/password", result2)  # Result will contain an existing user with a bad pass
        # Success
        self.assertEqual("User logged in", result3)  # Username and password exist in the database.

    def test_logout_success_(self):
        a = App(Login(DjangoInterface()), UserEdits(), CourseEdit())
        user = a.command("login testUsername testPassword")
        result = a.command("logout")
        self.assertEqual("User logged out", result)

    def test_logout_failed_not_loggedin(self):
        a = App(Login(DjangoInterface()), UserEdits(), CourseEdit())
        result = a.command("logout")
        self.assertEqual("User is not logged in", result)
        self.assertNotEqual("User logged out", result)

    def test_add_user(self):
        a = App(Login(DjangoInterface()), UserEdits(), CourseEdit())
        a.command("login brokenUsername brokenPassword")
        result1 = a.command("add_user newUsername newPassword 0000 address phonenum email")
        a.command("logout")
        a.command("login testUsername testPassword")
        result2 = a.command("add_user ***** newPassword 0000 address phonenum email")
        result3 = a.command("add_user username * 0000 address phonenum email")
        result4 = a.command("add_user newUsername newPassword 0000 address phonenum email")
        # Error cases
        self.assertEqual("Illegal permissions to do this action", result1)
        self.assertEqual("Failed to add user. Improper parameters", result2)
        self.assertEqual("Failed to add user. Improper parameters", result3)
        # Success
        self.assertEqual("User successfully added", result4)
        a.command("logout")

    def test_delete_user(self):
        a = App(Login(DjangoInterface()), UserEdits(), CourseEdit())

        a.command("login brokenUsername brokenPassword")
        result1 = a.command("delete_user delUsername")
        a.command("logout")
        a.command("login testUsername testPassword")
        result2 = a.command("delete_user BadUsername")
        result4 = a.command("delete_user delUsername")
        # Error cases
        self.assertEqual("Illegal permissions to do this action", result1)
        self.assertEqual("User unsuccessfully deleted", result2)
        # Success
        self.assertEqual("User successfully deleted", result4)
        a.command("logout")

    def test_change_contact_info(self):
        a = App(Login(DjangoInterface()), UserEdits(), CourseEdit())
        a.command("login testUsername testPassword")
        result1 = a.command("change_contact testUsername name SAUCE")
        result2 = a.command("change_contact testUsername username *")
        result3 = a.command("change_contact testUsername address newaddress")
        # Error cases
        self.assertEqual("Illegal changed field", result1)  # Tried to change an illegal field
        self.assertEqual("Invalid parameter for this command",
                         result2)  # Updated field was illegal, contact field valid.
        # Success
        self.assertEqual("Contact information changed", result3)

    def test_edit_user_no_permissions(self):
        a = App(Login(DjangoInterface()), UserEdits(), CourseEdit())
        a.command("login brokenUsername brokenPassword")
        result = a.command("edit_user username field update")
        # Error cases
        self.assertEqual("Illegal permissions to do this action", result)

    def test_edit_user_does_not_exist(self):
        a = App(Login(DjangoInterface()), UserEdits(), CourseEdit())
        a.command("login testUsername testPassword")
        result = a.command("edit_user userdne username field")
        # Error cases
        self.assertEqual("Failed to update user", result)

    def test_edit_user_illegal(self):
        a = App(Login(DjangoInterface()), UserEdits(), CourseEdit())
        a.command("login testUsername testPassword")
        result = a.command("edit_user userdne namedne field")
        self.assertEqual("Tried to change illegal field", result)  # Tried to change an illegal field

    def test_edit_user_success(self):
        a = App(Login(DjangoInterface()), UserEdits(), CourseEdit())
        a.command("login testUsername testPassword")
        result = a.command("edit_user testUsername username newname")
        self.assertEqual("User successfully updated", result)  # Tried to change an illegal field

    def send_email(self):
        a = App(Login(DjangoInterface()), UserEdits(), CourseEdit())
        result = a.command("From To Subject Body User UpdatedUser")
        # Error cases
        self.assertEqual("From user does not exist", result)
        self.assertEqual("To user does not exist", result)
        self.assertEqual("Illegal email subject", result)
        self.assertEqual("Illegal email body", result)
        # Success
        self.assertEqual("Email successfully sent", result)

    def test_send__TA_email(self):
        a = App(Login(DjangoInterface()), UserEdits(), CourseEdit())
        result = a.command("From To Subject Body TA UpdatedUser")
        # Error cases
        self.assertEqual("Illegal permissions to do this activity", result)
        self.assertEqual("TA(s) do not exist", result)
        self.assertEqual("Illegal email subject", result)
        self.assertEqual("Illegal email body", result)
        # Success
        self.assertEqual("Email sent to TA(s) successfully", result)

    # Course Edits tests
    def test_view__all_classes(self):
        a = App(Login(DjangoInterface()), UserEdits(), CourseEdit())
        result = a.command("LoggedInUser")
        # Error cases
        self.assertEqual("Not enrolled in any classes", result)
        # Success
        self.assertEqual("List of classes: ", result)

    def test_assign_TA(self):
        a = App(Login(DjangoInterface()), UserEdits(), CourseEdit())
        a.command("login brokenUsername brokenPassword")
        result1 = a.command("add_TA_to_course testCourse TAUsername")
        a.command("logout")
        a.command("login testUsername testPassword")
        result2 = a.command("add_TA_to_course testCourse badTA")
        result3 = a.command("add_TA_to_course badCourse TAUsername")
        result4 = a.command("add_TA_to_course testcourse 101 badLab")
        result5 = a.command("add_TA_to_course testCourse TAUsername")
        # Error cases
        self.assertEqual("Illegal permissions to do this action", result1)
        self.assertEqual("TA does not exist", result2)
        self.assertEqual("Failed to add TA to course.", result3)
        # self.assertEqual("Lab section Does not exist", result4)
        # Success
        self.assertEqual("TA successfully added to course", result5)
        a.command("logout")

    def test_create_course(self):
        a = App(Login(DjangoInterface()), UserEdits(), CourseEdit())
        a.command("login brokenUsername brokenPassword")
        result1 = a.command("create_course testUsername testCourse 10:00 10:50")
        a.command("logout")
        a.command("login testUsername testPassword")
        result2 = a.command("create_course testUsername testCourse 10:00 10:50")
        result3 = a.command("create_course testUsername badTime 10:50")
        result4 = a.command("create_course testUsername 10:00 badTime")
        result5 = a.command("create_course testUsername testcourse 10:00 10:50")
        result6 = a.command("create_course testUsername testCourse 10:00 10:50")
        # Error cases
        self.assertEqual("Illegal permissions to do this action", result1)
        #  self.assertEqual("Illegal start time entered", result3)
        # self.assertEqual("Illegal end time entered", result4)
        # Success
        self.assertEqual("Course successfully added", result6)
        a.command("logout")

    def test_delete_course(self):
        a = App(Login(DjangoInterface()), UserEdits(), CourseEdit())
        a.command("login brokenUsername brokenPassword")
        result1 = a.command("delete_course testCurse")
        a.command("logout")
        a.command("login testUsername testPassword")
        result2 = a.command("delete_course badID")
        result3 = a.command("delete_course testCourse")
        # Error cases
        self.assertEqual("Illegal permissions to do this action", result1)
        self.assertEqual("Course unsuccessfully deleted", result2)
        # Success
        self.assertEqual("Course successfully deleted", result3)



    # DataRetrieval
    def test_ViewDatabase(self):
        a = App(Login(DjangoInterface()), UserEdits(), CourseEdit())
        result = a.command("LoggedInUser")
        # Error cases
        self.assertEqual("Illegal permissions to do this activity", result)
        self.assertEqual("Error while connecting to the database", result)
        # Success
        self.assertEqual("Data gathered", result)
