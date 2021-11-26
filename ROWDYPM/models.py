from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# This is updating the database, need to change it out for something that will
# update NoSQL db, either DynamoDB or mongoDB. 
# Also need to edit settings.py with DynamoDB or mongoDB config
class Password(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    URL_logo = models.CharField(max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]