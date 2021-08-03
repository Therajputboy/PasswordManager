from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Safe(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    site_name = models.CharField(max_length=100)
    site_url = models.CharField(max_length=200)
    site_username = models.CharField(max_length=50)
    site_text = models.CharField(default="",max_length=200)
    site_password = models.CharField(max_length=300)


    def __str__(self):
        return self.site_name +" - Safe"
