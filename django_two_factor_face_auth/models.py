from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import time
import os

def content_file_name(instance, filename):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    name, extension = os.path.splitext(filename)
    return os.path.join('content', instance.user.username, timestr + extension)

def content_ufile_name(instance, filename):
    name, extension = os.path.splitext(filename)
    return os.path.join('content', instance.user.username, filename)

class UserFaceImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to=content_file_name, blank=False)

class UserFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ufile = models.FileField(upload_to=content_ufile_name, blank=False)
    def ufilename(self):
        return os.path.basename(self.ufile.name)

@receiver(post_delete, sender=UserFile)
def submission_delete(sender, instance, **kwargs):
    instance.ufile.delete(False) 