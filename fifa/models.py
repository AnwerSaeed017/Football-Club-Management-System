from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model


User=get_user_model()

class Profile(models.Model):  # Class names should be in CamelCase
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    emailaddress = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username  # Assuming 'User' model has a 'username' field
