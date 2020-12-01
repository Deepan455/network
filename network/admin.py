from django.contrib import admin

# Register your models here.
from .models import User,Posts,Image

admin.site.register(User)
admin.site.register(Posts)
admin.site.register(Image)