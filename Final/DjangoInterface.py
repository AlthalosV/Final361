from Final.models import *
from django.db import models
from WorkingModels.CourseInfo import CourseInfo
from WorkingModels.LabInfo import LabInfo
from WorkingModels.UserInfo import UserInfo


class DjangoInterface:

    # Getters
    def login_username(self, username):
        user = User.objects.get(username=username)
        if user is None:
            return "User invalid"
        return user

    def login_password(self, passwordP):
        retPass = User.objects.get(password=passwordP)
        if retPass is None:
            return "password invalid"
        return retPass.password

    def user_permissions(self, permissionP):
        retPermissions = User.objects.get(permissions=permissionP)
        if retPermissions.permissions is None:
            return "address DNE"
        return retPermissions.permissions

    def user_address(self, addressP):
        retAddress = User.objects.get(address=addressP)
        if retAddress.address is None:
            return "address DNE"
        return retAddress.address

    def user_email(self, emailP):
        retEmail = User.objects.get(email=emailP)
        if retEmail.email is None:
            return "email DNE"
        return retEmail.email

    def user_phoneNum(self, phoneNumP):
        retPhoneNum = User.objects.get(phonenumber=phoneNumP)
        if retPhoneNum.phonenumber is None:
            return "Phone number DNE"
        return retPhoneNum.phonenumber

    # Course functions
    def course_ID(self, courseIDP):
        retID = Course.objects.get(courseId=courseIDP)
        if retID.courseId is None:
            return "Course ID DNE"
        return retID.courseId

    def course_startTime(self, startTimeP):
        retStartTime = Course.objects.get(startTime=startTimeP)
        if retStartTime is None:
            return "Start time DNE"
        return retStartTime.startTime

    def course_endTime(self, endTimeP):
        retEndTime = Course.objects.get(endTime=endTimeP)
        if retEndTime is None:
            return "End time DNE"
        return retEndTime.endTime

    def get_all_courses(self):
        all_courses = Course.objects.all()
        List = []
        for course in all_courses:
            List.append(
                CourseInfo(course_name=course.courseId, instructor=course.instructor, start_time=course.startTime,
                           end_time=course.endTime, tas_per_course=course.TAsInCourse.all(),
                           students_per_course=course.studentsInCourse.all(),
                           labs_per_course=Lab.objects.filter(ParentCourse=course)))
        return List

    def get_all_classes_by_instructor(self, instructor_name):
        try:
            all_courses_with_this_instructor = Course.objects.filter(instructor=instructor_name)
        except Exception as e:
            return []
        course_list = []
        for course in all_courses_with_this_instructor:
            course_list.append(
                CourseInfo(course_name=course.courseId, instructor=course.instructor, start_time=course.startTime,
                           end_time=course.endTime,
                           tas_per_course=course.TAsInCourse.all(), students_per_course=course.studentsInCourse.all(),
                           labs_per_course=Lab.objects.filter(ParentCourse=course)))
        return course_list

    def get_all_users_in_system(self):
        all_users = User.objects.all()
        user_list = []
        for user in all_users:
            user_list.append(UserInfo(user_name=user.username, password=user.password, permissions=user.permissions,
                                      address=user.address, email=user.email, phone_number=user.phonenumber))
        return user_list

    def get_all_labs(self):
        all_labs = Lab.objects.all()
        lab_list = []
        try:
            for lab in all_labs:
                lab_list.append(LabInfo(lab_number=lab.labNumber, ta=lab.TA, students_per_lab=lab.studentsInLab.all(),
                                      start_time=lab.startTime, end_time=lab.endTime, parent_course=lab.ParentCourse))
        except Exception as e:
            return lab_list
        return lab_list

    def getCourse(self, courseIDP):
        retCourse = Course.objects.get(courseId=courseIDP)
        return retCourse

    def getLab(self, labNumberP):
        retLab = Lab.objects.get(labNumber=labNumberP)
        return retLab

    # Setters
    def create_user(self, UsernameP, PasswordP, PermissionsP, AddressP, PhoneNumberP, EmailP):
        U = User.objects.create(username=UsernameP, password=PasswordP, permissions=PermissionsP,
                                address=AddressP, phonenumber=PhoneNumberP, email=EmailP)
        U.save()

    def delete_user(self, UserNameP):
        U = User.objects.get(username=UserNameP)
        if U is not None:
            U.delete()
        else:
            print("Error: Invalid user, cannot delete")

    def update_user(self, UsernameP, FieldtoChange, UpdatedInfo):
        u = User.objects.get(username=UsernameP)
        if u is not None:
            if FieldtoChange == "username":
                u.username = UpdatedInfo
            elif FieldtoChange == "password":
                u.password = UpdatedInfo
            elif FieldtoChange == "permissions":
                u.permissions = UpdatedInfo
            elif FieldtoChange == "address":
                u.address = UpdatedInfo
            elif FieldtoChange == "phonenumber":
                u.phonenumber = UpdatedInfo
            elif FieldtoChange == "email":
                u.email = UpdatedInfo
            else:
                return "Tried to change illegal field"
        u.save()

    def create_course(self, instructorP, courseIDP, startTimeP, endTimeP):
        c = Course.objects.create(instructor=instructorP, courseId=courseIDP, startTime=startTimeP, endTime=endTimeP)
        c.save()

    def delete_course(self, courseIDP):
        c = Course.objects.get(courseId=courseIDP)
        if c is not None:
            c.delete()
        else:
            print("Error: Invalid course, cannot delete")

    def add_user_to_course(self, courseIDP, usernameP):
        c = Course.objects.get(courseId=courseIDP)
        u = User.objects.get(username=usernameP)
        c.studentsInCourse.add(u)
        c.save()

    def add_TA_to_course(self, courseIDP, TAnameP):
        c = Course.objects.get(courseId=courseIDP)
        u = User.objects.get(username=TAnameP)
        c.TAsInCourse.add(u)
        c.save()

    def assign_instructor_to_course(self, courseIDP, instructorP):
        c = Course.objects.get(courseId=courseIDP)
        c.instructor = instructorP
        c.save()

    def update_course(self, CourseIDP, FieldtoChange, UpdatedInfo):
        c = Course.objects.get(courseId=CourseIDP)
        if c is not None:
            if FieldtoChange == "courseId":
                c.courseId = UpdatedInfo
            elif FieldtoChange == "startTime":
                c.startTime = UpdatedInfo
            elif FieldtoChange == "endTime":
                c.endTime = UpdatedInfo
            else:
                return "Tried to change illegal field"
        c.save()

    def create_lab(self, labnumberP, TAnameP, startTimeP, endTimeP):
        l = Lab.objects.create(labNumber=labnumberP, TA=TAnameP, startTime=startTimeP, endTime=endTimeP)
        l.save()

    def delete_lab(self, labnumberP):
        l = Lab.objects.get(labNumber=labnumberP)
        if l is not None:
            l.delete()
        else:
            print("Error: Invalid lab, cannot delete")

    def add_student_to_lab(self, labP, studentP):
        labP.studentsInLab.add(studentP)
        studentP.save()

    def assign_ta_to_lab(self, labp, taP):
        l = Lab.objects.get(labNumber=labp)
        l.TA = taP
        l.save()

    def add_lab_section_to_course(self, labP, courseIDP):
        labP.ParentCourse = courseIDP
        labP.save()
