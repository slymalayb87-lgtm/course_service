from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    schedule = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name
