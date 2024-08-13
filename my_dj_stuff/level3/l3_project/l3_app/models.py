from django.db import models

# Create your models here.
class User(models.Model):
    top_name = models.CharField(max_length=256, unique=True)
    email = models.EmailField()

    def __str__(self):
        return self.top_name