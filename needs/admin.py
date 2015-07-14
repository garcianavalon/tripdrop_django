from django.contrib import admin
from needs import models
# Register your models here.

admin.site.register(models.ContactPerson)
admin.site.register(models.Country)
admin.site.register(models.Region)
admin.site.register(models.City)
admin.site.register(models.Need)
admin.site.register(models.Institution)