from django.db import models
from django.contrib.auth.models import User

class Folder(models.Model):
    folder_name = models.CharField(max_length=255)
    parent_folder = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    no_parent_folder = models.BooleanField(default=False)
    

class File(models.Model):
    file_name = models.CharField(max_length=255)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='user_files/')

