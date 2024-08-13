from django.db import models
from django.urls import reverse

# Create your models here.

class School(models.Model):
    name = models.CharField(max_length=256)
    principal = models.CharField(max_length=256)
    location = models.CharField(max_length=256)

    def get_absolute_url(self):
        return reverse("app1:school_detail", kwargs={'pk':self.pk})
    
    def __str__(self) -> str:
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=256)
    age = models.PositiveIntegerField()
    location = models.ForeignKey(School, 
                                 related_name='students',    # this is the name which will be used in the template
                                 on_delete=models.CASCADE)
    
    
    

    def __str__(self) -> str:
        return self.name