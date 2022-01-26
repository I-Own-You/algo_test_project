from distutils.command.upload import upload
from email.policy import default
from tokenize import blank_re
from django.db import models
from users.models import User


class Car(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='cars',null=True, blank=False)
    name = models.CharField(max_length=20, blank=False, null=True)
    description = models.CharField(max_length=300, blank=False, null=True)
    price = models.IntegerField(null=True, blank=False)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_changed = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

class Images(models.Model):
    owner = models.ForeignKey(Car, related_name='image', on_delete=models.CASCADE)
    images = models.ImageField(upload_to='cars/', default='cars/car_default.jpg',blank=True,null=True)
    
    def __str__(self):
        return self.images

