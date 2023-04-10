from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default='UNTITLED')
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title
