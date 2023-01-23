from django.contrib import admin

# Register your models here.
from .models.SNDGJob import SNDGJob,SNDGJobTrace
admin.site.register(SNDGJob)
admin.site.register(SNDGJobTrace)

