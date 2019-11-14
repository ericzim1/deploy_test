from __future__ import unicode_literals
from django.db import models
import datetime
from datetime import date
import re

class UserManager(models.Manager):
    def basic_validator(self,postData):
        errors={}
        if len(postData['first_name'])<3:
            errors['first_name']="First Name should be at least 2 characters"
        if not str.isalpha(postData['first_name']):
            errors['first_name']="First Name must be alpha"
        if len(postData['last_name'])<3:
            errors['last_name']="Last name should be at least 2 characters"
        if not str.isalpha(postData['last_name']):
            errors['last_name']="Last Name must be alpha"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):              
            errors['email'] = ("Invalid email address!")
        if len(postData['password']) < 8:
            errors['password']="Please enter a password with at least 8 characters"
        if postData['password'] != postData['confirm_pw']:
            errors['password'] ="Password does not match confirm password"
        if postData['birthdate'] > str(datetime.datetime.now()):
            errors['releasedt_input']="Please enter a birthdate that is earlier than today"
        x=User.objects.filter(email=postData['email'])
        if len(x)>0:
            errors['email']="Email provided is already registered"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    birthdate = models.DateField()
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    #liked_books = a list of books a given user likes
    #books_uploaded = a list of books uploaded by a given user

    def __repr__(self):
        return f"<User object: id: {self.id} first_name: {self.first_name} last_name: {self.last_name} birthdate: {self.birthdate} email:{self.email} >"


class BookManager(models.Manager):
    def book_validator(self,postData):
        errors={}
        if len(postData['new_title'])<1:
            errors['new_title']="Title should be at least 1 character"
        if len(postData['new_desc'])<5:
            errors['new_desc']="Description should be at least 5 characters"
        return errors

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded")
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    objects = BookManager()

    def __repr__(self):
        return f"<Book object: id: {self.id} title: {self.title} desc: {self.desc}>"