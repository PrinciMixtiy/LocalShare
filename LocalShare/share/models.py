from django.db import models
from django.contrib.auth import get_user_model

import os

User = get_user_model()

default_user_id = 0

def custom_file_name(instance, filename):
    return os.path.join('uploads', f'{instance.user.username}', filename)


class File(models.Model):
    FILE_TYPE = {
        'N': 'Normal',
        'D': 'Directory'
    }

    name = models.CharField(max_length=100)
    path = models.CharField(max_length=300)
    type = models.CharField(max_length=1, choices=FILE_TYPE)

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=default_user_id)
    
    def exists(self):
        return os.path.exists(self.path)

    def __str__(self):
        return f"{self.name} - {self.path[:30]} - {self.type}"


class UserFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=custom_file_name)
    shared = models.BooleanField(default=False)
    
    def switch_shared(self):
        self.shared = not self.shared
        self.save()
        
    def delete(self, *args, **kwargs):
        if self.file:
            self.file.delete(False)
        
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"
