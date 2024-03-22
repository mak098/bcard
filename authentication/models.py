from django.db import models

from django.contrib.auth.models import AbstractUser
from django.conf import settings
from Agency.models import Agency

class User(AbstractUser):
    agency = models.ForeignKey(Agency,null=True, blank=True,on_delete=models.PROTECT,related_name='user_agency' ,verbose_name='Agence' )
   
    class meta:
        app_label = "Users"
        db_table = "users"




