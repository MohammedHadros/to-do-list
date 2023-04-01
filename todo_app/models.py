from django.utils import timezone
from django.db import models

# Create your models here.

def one_week_hence():
    return timezone.now() + timezone.timedelta(days=7)

class List(models.Model):
    title=models.CharField(max_length=60)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Task(models.Model):
    list=models.ForeignKey(List,on_delete=models.CASCADE)
    title=models.CharField(max_length=60)
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    due_date=models.DateTimeField(auto_created=True , default=one_week_hence())

    def __str__(self):
        return self.title + " , " + str(self.due_date) 

