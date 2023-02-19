from django.contrib import admin
from StarWarsApp.models import DatasetCSV
import os


admin.site.site_title = "Star Wars"
admin.site.site_header = 'Star Wars'


class DatasetCSVAdmin(admin.ModelAdmin):
    '''
        Admin View
    '''
    list_display = ('created_date',)
    actions = ['delete_model',]

    @admin.action(description='Delete selected dataset and remove files from os')
    def delete_model(self, request, objs):
        for obj in objs:
            # remove file from os
            os.remove(os.path.join(obj.path.path))
            # remove obj from db
            obj.delete()


admin.site.register(DatasetCSV, DatasetCSVAdmin)
