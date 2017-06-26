from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .models import Users

def index(request):

		return render(request, "login/index.html")

def register(request):
	if request.method == "POST":
		db_result = Users.objects.register(request.POST)
		if not db_result["status"]:
			# print "not status***************"
			messages.add_message(request, messages.INFO, "Attempt to register failed.")
			for i in db_result["errors"]:
				messages.add_message(request, messages.INFO, "- " + i)
			return redirect(reverse("login:index"))
		else:
			# print "this is else!!***************"
			request.session["login_id"] = db_result["user"].id
			request.session["email"] = db_result["user"].email
			request.session["name"] = db_result["user"].name
			request.session["alias"] = db_result["user"].alias
			request.session["new_registration"] = 1
			return redirect(reverse("reviews:index"))
	else:
		return redirect(reverse("login:index"))

def login(request):
	if request.method == "POST":
		db_result = Users.objects.login(request.POST)
		if not db_result["status"]:
			messages.add_message(request, messages.INFO, "Login failed.")
			for i in db_result["errors"]:
				messages.add_message(request, messages.INFO, "- " + i)
			return redirect(reverse("login:index"))
		else:
			request.session["login_id"] = db_result["user"].id
			request.session["email"] = db_result["user"].email
			request.session["name"] = db_result["user"].name
			request.session["alias"] = db_result["user"].alias
			return redirect(reverse("reviews:index"))
	else:
		return redirect(reverse("login:index"))

def logout(request):
	request.session.clear()
	return redirect(reverse("login:index"))		















