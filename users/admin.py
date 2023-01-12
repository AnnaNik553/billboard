from django.contrib import admin

from .models import User, OneTimeCode

admin.site.register(User)
admin.site.register(OneTimeCode)
