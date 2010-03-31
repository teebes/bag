from django.db import models

class NamedUrl(models.Model):
    short_name = models.CharField(max_length=40)
    url_name = models.CharField(max_length=40)
    url_args = models.CharField(max_length=140, blank=True)
    
    redirect = models.BooleanField(default=False)
    
class ExternalUrl(models.Model):
    short_name = models.CharField(max_length=40)
    redirect_to = models.CharField(max_length=300)
