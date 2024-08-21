from django.contrib import admin
from . import models
# Register your models here.


class MovieAdmin(admin.ModelAdmin):
    fileds = [
        'title',
        'year',        
        'length'
    ]
    search_fields = ['year']
    list_filter = ['year']
    list_display = ['year', 'title', 'length']
    list_display_links = ['title']
    list_editable = ['year', 'length']


admin.site.register(models.Customer)
admin.site.register(models.Movie, MovieAdmin)