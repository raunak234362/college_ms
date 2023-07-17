"""
URL configuration for college_ms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf import settings as setting

from college_app import views, AdminViews, FacultyViews, StudentViews, forms

urlpatterns = [
                  path('demo', views.showDemoPage),
                  path('admin/', admin.site.urls),
                  path('', views.ShowLoginPage, name="show_login"),
                  path('get_user_details', views.GetUserDetails),
                  path('logout_user', views.logout_user, name="logout"),
                  path('doLogin', views.doLogin, name="do_login"),
                  path('admin_home', AdminViews.admin_home, name="admin_home"),
                  path('add_faculty', AdminViews.add_faculty, name="add_faculty"),
                  path('add_faculty_save', AdminViews.add_faculty_save, name="add_faculty_save"),
                  path('add_course', AdminViews.add_course, name="add_course"),
                  path('add_course_save', AdminViews.add_course_save, name="add_course_save"),
                  path('add_student', AdminViews.add_student, name="add_student"),
                  path('add_student_save', AdminViews.add_student_save, name="add_student_save"),
                  path('add_subject', AdminViews.add_subject, name="add_subject"),
                  path('add_subject_save', AdminViews.add_subject_save, name="add_subject_save"),
                  path('manage_faculty', AdminViews.manage_faculty, name="manage_faculty"),
                  path('manage_student', AdminViews.manage_student, name="manage_student"),
                  path('manage_course', AdminViews.manage_course, name="manage_course"),
                  path('manage_subject', AdminViews.manage_subject, name="manage_subject"),
                  path('edit_faculty/<str:faculty_id>', AdminViews.edit_faculty, name="edit_faculty"),
                  path('edit_faculty_save', AdminViews.edit_faculty_save, name="edit_faculty_save"),
                  path('edit_student/<str:student_id>', AdminViews.edit_student, name="edit_student"),
                  path('edit_student_save', AdminViews.edit_student_save, name="edit_student_save"),
                  path('edit_subject/<str:subject_id>', AdminViews.edit_subject, name="edit_subject"),
                  path('edit_subject_save', AdminViews.edit_subject_save, name="edit_subject_save"),
                  path('edit_course/<str:course_id>', AdminViews.edit_course, name="edit_course"),
                  path('edit_course_save', AdminViews.edit_course_save, name="edit_course_save"),
                  path('manage_session', AdminViews.manage_session, name="manage_session"),
                  path('add_session_save', AdminViews.add_session_save, name="add_session_save"),
                  path('student_feedback_message', AdminViews.student_feedback_message,name="student_feedback_message"),
                  path('faculty_feedback_message', AdminViews.faculty_feedback_message,name="faculty_feedback_message"),
                  path('admin_view_attendance', AdminViews.admin_view_attendance,name="admin_view_attendance"),
                  path('faculty_leave_view', AdminViews.faculty_leave_view,name="faculty_leave_view"),
                  path('student_approve_leave/<str:leave_id>', AdminViews.student_approve_leave,name="student_approve_leave"),
                  path('student_disapprove_leave/<str:leave_id>', AdminViews.student_disapprove_leave,name="student_disapprove_leave"),
                  path('faculty_disapprove_leave/<str:leave_id>', AdminViews.faculty_disapprove_leave,name="faculty_disapprove_leave"),
                  path('faculty_approve_leave/<str:leave_id>', AdminViews.faculty_approve_leave,name="faculty_approve_leave"),
                #   path('student_feedback_message_replied', AdminViews.student_feedback_message_replied,name="student_feedback_message_replied"),
                #   path('faculty_feedback_message_replied', AdminViews.faculty_feedback_message_replied,name="faculty_feedback_message_replied"),
                  # ------------------------    Faculty URL     --------------------------------
                  path('faculty_home', FacultyViews.faculty_home, name="faculty_home"),
                  path('faculty_take_attendance', FacultyViews.faculty_take_attendance, name="faculty_take_attendance"),
                  path('faculty_update_attendance', FacultyViews.faculty_update_attendance, name="faculty_update_attendance"),
                  path('faculty_apply_leave', FacultyViews.faculty_apply_leave, name="faculty_apply_leave"),
                  path('faculty_apply_leave_save', FacultyViews.faculty_apply_leave_save, name="faculty_apply_leave_save"),
                  path('faculty_feedback', FacultyViews.faculty_feedback, name="faculty_feedback"),
                  path('faculty_feedback_save', FacultyViews.faculty_feedback_save, name="faculty_feedback_save"),
                  # ------------------------    student URL     --------------------------------
                  path('student_home', StudentViews.student_home, name="student_home"),
                    path('media/<path:path>', AdminViews.MediaView.as_view(), name='media-view'),
              ]+ static(setting.MEDIA_URL, document_root=setting.MEDIA_ROOT) + static(setting.STATIC_URL,
                                                                                         document_root=setting.STATIC_ROOT)
