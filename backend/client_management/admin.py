from django.contrib import admin

# Register your models here.
from client_management import models
admin.site.register(models.discount_policy)
admin.site.register(models.Member)