from django.contrib import admin

# Import your models here.
from .models import Profile

# Register your models here.
admin.site.register(Profile)
