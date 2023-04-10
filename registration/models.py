from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass
User._meta.get_field('groups').remote_field.related_name = 'registration_user_groups'
User._meta.get_field('user_permissions').remote_field.related_name = 'registration_user_permissions'