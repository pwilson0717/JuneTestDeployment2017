from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages
from .models import Authors, Books, Reviews
from ..login.models import Users

def index(request):
	if "login_id" in request.session:
		context = {
			"recent_reviews": Reviews.objects.recent(),
			"all_books": Books.objects.all(),
		}

		return render(request, "reviews/index.html", context)
	else:
		return redirect(reverse("login:index"))

def add_book(request):
	if "login_id" in request.session:
		context = {
			"all_authors": Authors.objects.all(),
		}
		return render(request, "reviews/add_book.html", context)
	else:
		return redirect(reverse("reviews:index"))

def view_book(request, id):
	if "login_id" in request.session:
		context = {
			"book": Books.objects.get(id=id),
		}
		return render(request, "reviews/view_book.html", context)
	else:
		return redirect(reverse("reviews:index"))

def view_user(request, id):
	if "login_id" in request.session:
		context = {
			"user": Users.objects.get(id=id),
			"books_reviewed": Books.objects.filter(reviews__author_id=id).distinct(),
		}
		return render(request, "reviews/view_user.html")
	else:
		return redirect(reverse("reviews:index"))

def models_view(request):
	if "login_id" in request.session:
		context = {
			"all_users": User.objects.all(),
			"all_books": Books.objects.all(),
			"all_authors": Authors.objects.all(),
			"all_reviews": Reviews.objects.all(),
		}
		return render(request, "reviews/models_view.html", context)
	else:
		return redirect(reverse("reviews:index"))

def add_book_and_review(request):
	if "login_id" in request.session:
		if request.method == "POST":
			db_result = Books.objects.add_book_and_review(int(request.session["login_id"]), request.POST)
			if not db_result["status"]:
				for i in db_result["errors"]:
					messages.add_message(request, messages.INFO, "- " + i)
				return redirect(reverse("reviews:add_book"))
			else:
				return redirect(reverse("reviews:view_book", kwargs={'id': str(db_result["book"].id)}))
		else:
			return redirect(reverse("reviews:add_book"))
	else:
		return redirect(reverse("reviews:index"))

def add_review(request):
	if "login_id" in request.session:
		if request.method == "POST":
			Reviews.objects.add_review(int(request.session["login_id"]), request.POST)
			return redirect(request.META["HTTP_REFERER"])
		else:
			return redirect(request.META["HTTP_REFERER"])

	else: 
		return redirect(reverse("reviews:index"))

def delete_review(request, id):
	if "login_id" in request.session:
		Reviews.objects.remove(id)
		return redirect(request.META["HTTP_REFERER"])
	else:
		return redirect(reverse("reviews:index"))

def catcher(request):
	return redirect(reverse("reviews:index"))












