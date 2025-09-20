from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # store hashed password ideally

    def __str__(self):
        return self.email
