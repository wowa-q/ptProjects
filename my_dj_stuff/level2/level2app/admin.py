from django.contrib import admin

from level2app.models import AccessRecord, Topic, Webpage

# Register your models here.
admin.site.register(AccessRecord)
admin.site.register(Topic)
admin.site.register(Webpage)