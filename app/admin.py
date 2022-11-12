from django.contrib import admin

# Register your models here.
from app.models import real_time


@admin.register(real_time)
class appAdmin(admin.ModelAdmin):
     list_display = ['id','tik', 'cell_1', 'cell_2','cell_3','cell_4','cell_5',
     'cell_6','cell_7','cell_8','cell_9','cell_10']
     list_display_links = ['id', 'tik']
     list_per_page = 300