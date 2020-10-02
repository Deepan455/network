from django.contrib import admin

# Register your models here.
from .models import User,Profile,Posts

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Posts)