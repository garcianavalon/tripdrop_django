from django.contrib import admin
from needs import models as need_models

admin.site.register(need_models.City)
admin.site.register(need_models.Region)