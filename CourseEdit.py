
from Final import DjangoInterface
from Final.models import *

class CourseEdit:
    def __init__(self):
        self = self

    def create_course(self, instructor, coursename, starttime, endtime, logged_in_user):
        if logged_in_user.permissions[0] != '1' and logged_in_user.permissions[1] != '1':
            return "Illegal permissions to do this action"
        #Further error checking here
        try:
            DjangoInterface.DjangoInterface.create_course(self, instructor, coursename, starttime, endtime,)
        except Exception as e:
            print(e)
            return "Failed to create course."
        return "Course successfully added"  # Whatever was written in the acceptance tests

    def delete_course(self, courseToDel, logged_in_user):
        if logged_in_user.permissions[0] != '1' and logged_in_user.permissions[1] != '1':
            return "Illegal permissions to do this action"
        try:
            DjangoInterface.DjangoInterface.delete_course(self, courseToDel)
        except Exception as e:
            return "Course unsuccessfully deleted"
        return "Course successfully deleted"

    def add_user_to_course(self, courseIDP, userToAddP, logged_in_user):
        if logged_in_user.permissions[0] != '1' and logged_in_user.permissions[1] != '1':
            return "Illegal permissions to do this action"
        #Further error checking here
        try:
            DjangoInterface.DjangoInterface.add_user_to_course(self, courseIDP, userToAddP)
        except Exception as e:
            print(e)
            return "Failed to add user to course."
        return "Course successfully added"

    def view_all_courses(self, loggedinuser):
        return "yes"

    def assign_ta(self, tausername, courseid, labsection, loggedinuser):
        return "yes"

    def view_course_assignments(self, courseid, loggedinuser):
        return "yes"


