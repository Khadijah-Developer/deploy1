from django.db import models
from django.db import models
import re
from django.core.exceptions import ObjectDoesNotExist
import bcrypt
from datetime import datetime
# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
         errors = {}
         if len(postData["name"]) < 3 and not postData["name"].isalpha() :
                errors["name"] = "The name should be at least 3 characters and string"
         if len(postData["username"]) < 3 and not postData["username"].isalpha():
            errors["username"] = "The username should be at least 3 characters and string"

         username_exist = User.objects.filter(username = postData['username']) #username should be unique
         if len(username_exist)>0:
            errors["not_unique_username"] = "This username is already used!"

         if len(postData["pass"]) < 8:
                errors["pass"] = "Password should be at least 8 characters!"
         if postData["pass"] != postData["cpass"]:
            errors["password_not_match"] = "The passwords do not match!"

         if not postData['date']:
                errors['date2'] = "Please enter date Hired"
         return errors




class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Item(models.Model):
    item = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="Items", on_delete=models.CASCADE) #one to many 
    user_fav = models.ManyToManyField(User, related_name="fav_item") #many to many 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager() 