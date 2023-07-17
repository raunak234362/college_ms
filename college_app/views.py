import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from college_app.EmailBackEnd import EmailBackEnd
from django.urls import reverse


# from django.http import HttpResponse
#
#
# # Create your views here.
# def showDemoPage(request):
#     return HttpResponse("<h2>Demo Page</h2>")


# Create your views here.
def showDemoPage(request):
    return render(request, "demo.html")


def ShowLoginPage(request):
    return render(request, "login_page.html")


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
        if user != None:
            login(request, user)
            if user.user_type=="1":
                return HttpResponseRedirect('/admin_home')
            elif user.user_type=="2":
                return HttpResponseRedirect(reverse("faculty_home"))
            else:
                return HttpResponseRedirect(reverse("student_home"))
        else:
            messages.error(request,'Invalid Login Details')
            return HttpResponseRedirect("/")


def GetUserDetails(request):
    if request.user != None:
        return HttpResponse("User : " + request.user.email + " userstype : " + request.user.user_type)
    else:
        return HttpResponse("Please Login First")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")
