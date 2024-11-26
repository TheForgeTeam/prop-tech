from django.db import models

# Create your models here.

class Property(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    owner = models.CharField(max_length=100)
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
