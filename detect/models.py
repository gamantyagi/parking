from django.db import models
from django.contrib.auth.models import User


class details(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/temp_files')


class ImageOb(models.Model):
    image = models.ImageField(upload_to='temp_objects')
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
