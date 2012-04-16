from django.contrib import admin

from models import AestheticOptions

class AestheticOptionsAdmin(admin.ModelAdmin):
    list_display = ['name', 'option_list']
    list_editable = ['option_list']

admin.site.register(AestheticOptions, AestheticOptionsAdmin)
