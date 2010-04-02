from django.db import models

class BaseUrl(models.Model):
    short_name = models.CharField(max_length=40, unique=True)
    
class NamedUrl(BaseUrl):
    url_name = models.CharField(max_length=40)
    url_args = models.CharField(max_length=140, blank=True)
    redirect = models.BooleanField(default=False)
    
class ExternalUrl(BaseUrl):
    redirect_to = models.CharField(max_length=300)
