from django.db import models


class Setting(models.Model):
    
    name = models.CharField(max_length=50, unique=True, blank=False)
    value = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f'{self.name}: {self.value}'
    