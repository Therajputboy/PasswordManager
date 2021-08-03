from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	image = models.ImageField(default='default.jpg',upload_to='profile_pics')
	master_key = models.CharField(default="",max_length=128)
	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self,*args,**kwargs):
		super(Profile,self).save(*args,**kwargs)

		img = Image.open(self.image.path)
		if img.height > 200 or img.width >200:
			output_size = (200,200)
			img.thumbnail(output_size)
			img.save(self.image.path)

class AuthToken(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + 'AuthToken'