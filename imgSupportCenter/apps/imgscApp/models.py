from django.db import models
from datetime import datetime
import re, bcrypt
# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9+-_.]+\.[a-zA-Z]+$')

class Validator(models.Manager):
    def validate(self, formData):
        errors = []
        
        #First Name
        if len(formData["firstName"]) < 1:
            errors.append("Invalid First Name")
        elif len(formData["firstName"]) < 2:
            errors.append(formData["Must be at least two charachters"])
        
        #Last Name
        if len(formData["lastName"]) < 1:
            errors.append(["Invalid Last name"])
        elif len(formData["lastName"]) < 2:
            errors.append("Last must be at least 2 charachters")
        #Billing Address
        if len(formData["billingAdd"]) < 1:
            errors.append("Can't be empty")
        elif len(formData["billingAdd"]) < 2:
            errors.append("Invalid address")

        #DoB validate later
        
        #Email Validation
        if len(formData["email"]) < 1:
            errors.append("Invalid Email")
        elif not EMAIL_REGEX.match(formData["email"]):
            errors.append("Please type correct email")
        else:
            if len(User.objects.filter(email=formData["email"].lower()))>0:
                errors.append("Email already in use")
        #Password Validation
        if len(formData["password"]) <1:
            errors.append("Password can't be blank")
        elif len(formData["password"]) < 8:
            errors.append("Password Must be at least eight characters")
        #Reconfirmation Password
        if formData["password"] != formData["confirmPassword"]:
            errors.append("Password didn't match")

        #Final Check
        if len(errors) > 0:
            return (False, errors)
        else:
            hashed_pw = bcrypt.hashpw(formData["password"].encode(), bcrypt.gensalt())
            user = User.objects.create(
                firstName = formData["firstName"],
                lastName = formData["lastName"],
                email = formData["email"],
                billingAdd = formData["billingAdd"],
                password = formData["password"],
                dateOfBirth = formData["dateOfBirth"]
            )
            return (True, user)

class User(models.Model):
    firstName = models.CharField(max_length = 255);
    lastName = models.CharField(max_length = 255)
    dateOfBirth = models.CharField(max_length=10)
    email = models.CharField(max_length = 255)
    billingAdd = models.CharField(max_length=255) #2018/05/02
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = Validator()

    