from __future__ import unicode_literals
from django.db import models
import re
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
import bcrypt

def get_pw_hash(pw, salt = bcrypt.gensalt()):
	return(bcrypt.hashpw(pw, salt))


class UsersManager(models.Manager):
	def register(self, postData):
		errors = []

		if len(postData["email"]) < 1:
			errors.append("Your emal is required.")
		elif not email_regex.match(postData["email"]):
			errors.append("Incorrectly formed email.")

		elif len(self.filter(email= postData["email"])) > 0:
			errors.append("The email ({}) is already used.".format(postData["email"]))

		if len(postData["name"]) < 1:
			errors.append("The name field is empty.")

		if len(postData["name"]) < 1:
			errors.append("Your name is required.")

		if len(postData["alias"]) < 1:
			errors.append("Your alias name is required.")

		if len(postData["pw_1"]) < 1:
			errors.append("Your password is required.")
		elif len(postData["pw_1"]) < 8:
			errors.append("Your password must be at least 8 characters.")
		elif not re.match(r'^.*[A-Z]+.*$', postData['pw_1'] ):
			errors.append("The password must contain at least 1 capital letter.")
		elif not re.match(r'^.*\d+.*$', postData['pw_1']):
			errors.append("The password must contain at least 1 number.")

		if postData["pw_1"] != postData["pw_2"]:
			errors.append("The passwords do not match.")

		if len(errors):
			return {
				"status": False,
				"errors": errors
			}
		else:
			return {
				"status": True,
				"user": self.create(
					email = postData["email"],
					name = postData["name"],
					alias = postData["alias"],
					password = get_pw_hash(postData["pw_1"].encode()),
					)
			}

	def login(self, postData):
		errors = []

		if len (postData["email"]) < 1:
			errors.append("Your email is required.")
		elif not email_regex.match(postData["email"]):
			errors.append("email format is incorrect.")
		elif len (self.filter(email = postData["email"])) < 1:
			errors.append("Unknown email.")

		elif len(postData["pw"]) < 1:
			errors.append("Your password is required.")
		else:
			user = self.get(email = postData["email"])
			if get_pw_hash(postData["pw"].encode(), user.password.encode()) != user.password:
				errors.append("Incorrect email or password.")

		if len (errors):
			return {
				"status": False,
				"errors": errors
			}
		else:
			return {
				"status": True,
				"user": self.get(email = postData["email"])
			}

class Users(models.Model):
	name = models.CharField(max_length = 255)
	alias = models.CharField(max_length = 255)
	email = models.CharField(max_length = 255)
	password = models.CharField(max_length = 50)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	objects = UsersManager()

