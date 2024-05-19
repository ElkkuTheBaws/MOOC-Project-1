from django.db import models
from django.contrib.auth.models import User
from django import forms

class Receipt(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	amount = models.TextField()
	content = models.TextField()

class CreateUserForm(forms.Form):
	username = forms.CharField(label="Your username",min_length=3, max_length=20)
	email = forms.EmailField()
	password = forms.CharField(label="Password",min_length=5, max_length=30, widget=forms.PasswordInput())