from django.contrib import admin

from .models import UserFaceImage, UserFile

admin.site.register(UserFaceImage)
admin.site.register(UserFile)