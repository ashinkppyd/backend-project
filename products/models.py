from django.db import models

# Create your models here.
class Watch(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20)
    image = models.URLField(blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.name
