from django.contrib import admin

from rooturls.models import ExternalUrl, NamedUrl

admin.site.register(ExternalUrl)
admin.site.register(NamedUrl)