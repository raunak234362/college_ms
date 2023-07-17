import datetime
import json

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import AddStudentForm, EditStudentForm
from .models import Attendance, AttendanceReport, CustomUser, Courses, FeedBackFaculty, FeedBackStudent, LeaveReportFaculty, LeaveReportStudent, Subjects, Faculty, Students, SessionYearModel

from django.http import HttpResponseNotFound
from django.views.generic import View
from django.conf import settings


class MediaView(View):
    def get(self, request, path):
        try:
            with open(settings.MEDIA_ROOT + '/' + path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='image/jpeg')
                return response
        except IOError:
            return HttpResponseNotFound('File not found')


def admin_home(request):
    return render(request, "hod_template/home_content.html")


def add_faculty(request):
    return render(request, "hod_template/add_faculty_template.html")


def add_faculty_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                  last_name=last_name, first_name=first_name, user_type=2)
            user.is_faculty = True
            user.save()
            messages.success(request, "Successfully Added Faculty")
            return HttpResponseRedirect(reverse("add_faculty"))
        except Exception as e:
            print(e)
            messages.error(request, "Failed to Add faculty")
            return HttpResponseRedirect(reverse("add_faculty"))


def add_course(request):
    return render(request, "hod_template/add_course_template.html")


def add_course_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        course = request.POST.get("course")

        try:
            course_model = Courses()
            course_model.course_name = course
            # Courses.objects.create(course_model)
            # course_model.save()
            # course_model.is_course = True
            course_model.save()
            messages.success(request, "Successfully Added Course")
            return HttpResponseRedirect(reverse("add_course"))

        except Exception as e:
            print(e)
            messages.error(request, "Failed To Add Course")
            return HttpResponseRedirect(reverse("add_faculty"))


def add_student(request):
    courses = Courses.objects.all()
    form = AddStudentForm()
    data = [
        {
            'id': course.id,
            'name': course.course_name
        }
        for course in courses]
    return render(request, "hod_template/add_student_template.html", {"courses": data, "form": form})


def add_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            session_year_id = form.cleaned_data["session_year_id"]
            course_id = form.cleaned_data["course"]
            gender = form.cleaned_data["gender"]
            address = request.POST.get("address")
            course_obj = Courses.objects.get(id=course_id)

            # if request.FILES.get('profile_pic', False):
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
            
            # else:
            #     profile_pic_url = None

            # try:
            Students = Students.objects.create_user(
                username=username,
                email=email,
                password=password,
                last_name=last_name,
                first_name=first_name,
                gender=gender,
                profile_pic=profile_pic_url,
                course=course_obj.id,
                session_year_id=session_year_id,
                address=address
                )
                
            messages.success(request, "Successfully Added Student")
            return HttpResponseRedirect(reverse("add_student"))
            # except Exception as e:
            #     print(e)
            #     messages.error(request, "Failed to Add Student")
            #     return HttpResponseRedirect(reverse("add_student"))
        else:
            # Form is not valid, render it with errors
            # return render(request, "hod_template/add_student_template.html", {"form": form})
            # return HttpResponse("Invalid Form Data")  # Return a response for invalid form data  
            form = AddStudentForm(request.POST)
            return render(request, "hod_template/add_student_template.html", {"form": form})


def add_subject(request):
    courses = Courses.objects.all()
    data = [
        {
            'id': course.id,
            'name': course.course_name
        }
        for course in courses]
    faculties = CustomUser.objects.filter(user_type=2)
    data2 = [
        {
            'id': faculty.id,
            'first_name': faculty.first_name,
            'last_name': faculty.last_name
        }
        for faculty in faculties]
    return render(request, "hod_template/add_subject_template.html", {"faculty": data2, "courses": data})


def add_subject_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_name = request.POST.get("subject_name")
        course_id = request.POST.get("course")
        course_obj = Courses.objects.get(id=int(course_id))
        print(course_id)
        faculty_id = request.POST.get("faculty")
        faculty = CustomUser.objects.get(id=faculty_id)

        try:
            subject = Subjects(subject_name=subject_name, course_id_id=course_obj.id, faculty_id_id=faculty.id)
            subject.save()
            messages.success(request, "Successfully Added Subject")
            return HttpResponseRedirect(reverse("add_subject"))
        except Exception as e:
            print(e)
            messages.error(request, "Failed to Add Subject")
            return HttpResponseRedirect(reverse("add_subject"))


def manage_faculty(request):
    faculty = Faculty.objects.all()
    return render(request, "hod_template/manage_faculty_template.html", {"faculty": faculty})


def manage_student(request):
    students = Students.objects.all()
    student = [
        {
            'id': stud.id,
            'first_name': stud.admin.first_name,
            'last_name': stud.admin.last_name,
            'username': stud.admin.username,
            'gender': stud.gender,
            'profile_pic': stud.profile_pic,
            'session_start_year': stud.session_year_id.session_start_year,
            'session_end_year': stud.session_year_id.session_end_year,
            'course_name': stud.course_id.course_name,
            'last_login': stud.admin.last_login,
            'date_joined': stud.admin.date_joined
        }
        for stud in students
    ]
    print(student)
    return render(request, "hod_template/manage_student_template.html", {"students": student})


def manage_course(request):
    course = Courses.objects.all()
    return render(request, "hod_template/manage_course_template.html", {"courses": course})


def manage_subject(request):
    subject = Subjects.objects.all()
    return render(request, "hod_template/manage_subject_template.html", {"subjects": subject})


def edit_faculty(request, faculty_id):
    faculty = Faculty.objects.get(admin=faculty_id)
    return render(request, "hod_template/edit_faculty_template.html", {"faculty": faculty})


def edit_faculty_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        faculty_id = request.POST.get("faculty_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")

        try:
            user = CustomUser.objects.get(id=faculty_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            faculty_model = Faculty.objects.get(admin=faculty_id)
            faculty_model.save()
            messages.success(request, "Successfully Edited Faculty")
            return HttpResponseRedirect(reverse("edit_faculty" ,kwargs={"faculty_id":faculty_id}))
        except:
            messages.error(request, "Failed to Edit Faculty")
            return HttpResponseRedirect(reverse("edit_faculty" ,kwargs={"faculty_id":faculty_id}))
 

def edit_student(request, student_id):
    request.session['student_id']=student_id
    courses = Courses.objects.all()
    student = Students.objects.get(id=student_id)
    form = EditStudentForm()
    form.fields['student_id'].initial = student_id
    form.fields['email'].initial = student.admin.email
    form.fields['first_name'].initial = student.admin.first_name
    form.fields['last_name'].initial = student.admin.last_name
    form.fields['username'].initial = student.admin.username
    form.fields['address'].initial = student.address
    form.fields['Course'].initial = student.course_id.id
    form.fields['Gender'].initial = student.gender
    form.fields['session_start'].initial = student.session_year_id.session_start_year
    form.fields['session_end'].initial = student.session_year_id.session_end_year
    return render(request, "hod_template/edit_student_template.html",
                  {"form": form, "id": student_id,"username":student.admin.username})
    # courses = Courses.objects.all()
    # try:
    #     student = Students.objects.get(id=student_id)
    #     return render(request, "hod_template/edit_student_template.html", {"student": student, "courses": courses})
    # except Students.DoesNotExist:
    #     return HttpResponse("Student not found")


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id = request.session.get("student_id")
        if student_id==None:
            return HttpResponseRedirect("/manage_student")

        form=EditStudentForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            # session_year_id = form.cleaned_data["session_year"]
            session_start = form.cleaned_data["session_start"]
            session_end = form.cleaned_data["session_end"]
            course = form.cleaned_data["Course"]
            Gender = form.cleaned_data["Gender"]
            profile_pic_url = None

            if request.FILES.get('profile_pic', False):
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)

            try:
                print("==========================")
                print(student_id)
                student = Students.objects.get(id=student_id)
                user = CustomUser.objects.get(id=student.admin.id)
                print(user.first_name)
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.save()

                student.session_year_id.session_start_year = session_start
                student.session_year_id.session_end_year = session_end
                if (profile_pic_url is not None):
                    student.profile_pic = profile_pic_url
                student.Gender = Gender
                course = Courses.objects.get(id=course)
                student.course_id_id = course.id
                student.save()
                del request.session['student_id']
                messages.success(request, "Successfully Edited Student")
                return HttpResponseRedirect(reverse("edit_student", kwargs={"student_id":student_id}))
            except Exception as E:
                print(E)
                messages.error(request, "Failed to Edit Student")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
        else:
            form=EditStudentForm(request.POST)
            student=Students.object.get(admin=student_id)
            return render(request,"hod_template/edit_student_template.html",{"form":form,"id":student_id,"username":student.admin.username})


def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    course = Courses.objects.all()
    faculty = CustomUser.objects.filter(user_type=2)
    return render(request, "hod_template/edit_subject_template.html",
                  {"subject": subject, "faculty": faculty, "courses": course, "id": subject_id})


def edit_subject_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id = request.POST.get("subject_id")
        subject_name = request.POST.get("subject_name")
        faculty_id = request.POST.get("faculty")
        course_id = request.POST.get("course")

        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name
            faculty = CustomUser.objects.get(id=faculty_id)
            subject.faculty_id = faculty
            course = Courses.objects.get(id=course_id)
            subject.course_id = course
            subject.save()

            messages.success(request, "Successfully Edited Subject")
            return HttpResponseRedirect(reverse("/edit_subject/" ,subject_id))
        except Exception as E:
            print(E)
            messages.error(request, "Failed to Edit Subject")
            return HttpResponseRedirect(reverse("/edit_subject/" ,subject_id))


def edit_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    return render(request, "hod_template/edit_course_template.html", {"course": course, "id": course_id})


def edit_course_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        course_id = request.POST.get("course_id")
        course_name = request.POST.get("course")

        try:
            course = Courses.objects.get(id=course_id)
            course.course_name = course_name
            course.save()
            messages.success(request, "Successfully Edited Course")
            return HttpResponseRedirect(reverse("/edit_course/" ,course_id))
        except:
            messages.error(request, "Failed to Edit Course")
            return HttpResponseRedirect(reverse("/edit_course/" ,course_id))


def manage_session(request):
    return render(request, "hod_template/manage_session_template.html")


def add_session_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("manage_session"))
    else:
        session_start_year = request.POST.get("session_start")
        session_end_year = request.POST.get("session_end")

        try:
            sessionyear = SessionYearModel(session_start_year=session_start_year, session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Successfully Added Session")
            return HttpResponseRedirect(reverse("manage_session"))
        except:
            messages.error(request, "Failed to Add Session")
            return HttpResponseRedirect(reverse("manage_session"))


@csrf_exempt
def check_email_exist(request):
    email=request.POST.get("email")
    user_obj=CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_username_exist(request):
    username=request.POST.get("username")
    user_obj=CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)



def faculty_feedback_message(request):
    feedbacks=FeedBackFaculty.objects.all()
    return render(request,"hod_template/faculty_feedback_template.html",{"feedbacks":feedbacks})

def student_feedback_message(request):
    feedbacks=FeedBackStudent.objects.all()
    return render(request,"hod_template/student_feedback_template.html",{"feedbacks":feedbacks})

@csrf_exempt
def student_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

@csrf_exempt
def faculty_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBackFaculty.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def faculty_leave_view(request):
    leaves=LeaveReportFaculty.objects.all()
    return render(request,"hod_template/faculty_leave_view.html",{"leaves":leaves})

def student_leave_view(request):
    leaves=LeaveReportStudent.objects.all()
    return render(request,"hod_template/student_leave_view.html",{"leaves":leaves})

def student_approve_leave(request,leave_id):
    leave=LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))

def student_disapprove_leave(request,leave_id):
    leave=LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))


def faculty_approve_leave(request,leave_id):
    leave=LeaveReportFaculty.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("faculty_leave_view"))

def faculty_disapprove_leave(request,leave_id):
    leave=LeaveReportFaculty.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("faculty_leave_view"))



def admin_view_attendance(request):
    subjects=Subjects.objects.all()
    session_year_id=SessionYearModel.object.all()
    return render(request,"hod_template/admin_view_attendance.html",{"subjects":subjects,"session_year_id":session_year_id})

@csrf_exempt
def admin_get_attendance_dates(request):
    subject=request.POST.get("subject")
    session_year_id=request.POST.get("session_year_id")
    subject_obj=Subjects.objects.get(id=subject)
    session_year_obj=SessionYearModel.object.get(id=session_year_id)
    attendance=Attendance.objects.filter(subject_id=subject_obj,session_year_id=session_year_obj)
    attendance_obj=[]
    for attendance_single in attendance:
        data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date),"session_year_id":attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj),safe=False)


@csrf_exempt
def admin_get_attendance_student(request):
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    attendance_data=AttendanceReport.objects.filter(attendance_id=attendance)
    list_data=[]

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)
