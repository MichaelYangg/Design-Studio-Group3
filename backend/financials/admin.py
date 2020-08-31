from django.contrib import admin

# Register your models here.
from financials import models
admin.site.register(models.transaction)