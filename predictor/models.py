from django.db import models

# Create your models here.
from django.db import models

class Photo(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='photos/')
    predicted_disease = models.CharField(max_length=100)
