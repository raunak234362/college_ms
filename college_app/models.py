from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


#
# Create your models here.
class SessionYearModel(models.Model):
    id=models.AutoField(primary_key=True)
    session_start_year=models.DateField()
    session_end_year=models.DateField()
    object=models.Manager()


class CustomUser(AbstractUser):
    user_type_data = ((1, "admin"), (2, "Faculty"), (3, "Students"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Faculty(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, default=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Courses(models.Model):
    id=models.AutoField(primary_key=True)
    course_name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1)
    faculty_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class StudentManager(models.Manager):
    def create_user(self, username, email, last_name, first_name, profile_pic, gender, address, course, start_year=None,
                    end_year=None, password=None):
        user = CustomUser.objects.create_user(username=username, email=email,
                                              last_name=last_name, first_name=first_name, user_type=3)
        user.set_password(password)
        user.save(using=self._db)
        # print(user)
        year = SessionYearModel(session_start_year=start_year, session_end_year=end_year)
        year.save(using=self._db)
        student = self.model(admin=user, gender=gender, profile_pic=profile_pic, course_id_id=course, address=address,
                             session_year_id=year)
        student.save(using=self._db)


class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, default=3)
    gender = models.CharField(max_length=255)
    profile_pic = models.FileField()
    address = models.CharField(max_length=255, default=None)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    # session_start_year = models.DateField()
    # session_end_year=models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = StudentManager()


class Attendance(models.Model):
    # id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    attendance_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class AttendanceReport(models.Model):
    # id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.DO_NOTHING)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class LeaveReportStudent(models.Model):
    # id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    leave_date = models.CharField(max_length=255)
    leave_message = models.CharField(max_length=255)
    leave_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class LeaveReportFaculty(models.Model):
    # id = models.AutoField(primary_key=True)
    faculty_id = models.ForeignKey(Faculty, on_delete=models.DO_NOTHING)
    leave_date = models.CharField(max_length=255)
    leave_message = models.CharField(max_length=255)
    leave_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class FeedBackStudent(models.Model):
    # id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    feedback = models.CharField(max_length=255)
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class FeedBackFaculty(models.Model):
    # id = models.AutoField(primary_key=True)
    faculty_id = models.ForeignKey(Faculty, on_delete=models.DO_NOTHING)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class NotificationStudent(models.Model):
    # id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Faculty, on_delete=models.DO_NOTHING)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class NotificationFaculty(models.Model):
    # id = models.AutoField(primary_key=True)
    faculty_id = models.ForeignKey(Faculty, on_delete=models.DO_NOTHING)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # print(instance)
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Faculty.objects.create(admin=instance)
        if instance.user_type == 3:
            # return instance
            
                            Students.objects.create(admin=instance,course_id=Courses.objects.get(id=1),session_year_id=SessionYearModel.object.get(id=1),address="",profile_pic="",gender="")
       

#
# @receiver(post_save, sender=CustomUser)
# def save_user_profile(sender, instance, **kwargs):
#     if instance.user_type == 1:
#         Admin.save()
#     if instance.user_type == 2:
#         Faculty.save()
#     if instance.user_type == 3:
#         Students.save()
