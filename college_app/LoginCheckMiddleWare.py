from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "college_app.AdminViews":
                    pass
                elif modulename == "college_app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type == "2":
                if modulename == "college_app.FacultyViews":
                    pass
                elif modulename == "college_app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("faculty_home"))
            elif user.user_type == "3":
                if modulename == "college_app.StudentViews":
                    pass
                elif modulename == "college_app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("student_home"))
            else:
                return HttpResponseRedirect(reverse("show_login"))

        else:
            if request.path == reverse("show_login") or request.path == reverse("do_login"):
                pass
            else:
                return HttpResponseRedirect(reverse("show_login"))
