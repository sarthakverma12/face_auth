from django.contrib import admin

from .models import UserFaceImage, UserFile,Profile

admin.site.register(UserFaceImage)
admin.site.register(UserFile)
admin.site.register(Profile)