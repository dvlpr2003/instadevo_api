from django.db import models

# Create your models here.


class UploadMedia(models.Model):
    name = models.CharField(max_length = 40)
    
    
