from user.models import AuthToken
from django.contrib import admin
from .models import AuthToken,Profile
# Register your models here.
admin.site.register(AuthToken)
admin.site.register(Profile)