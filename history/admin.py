from django.contrib import admin
from . import models


class HistoryAdmin(admin.ModelAdmin):
    list_display = ('entity', 'record', 'new_tax',)
    search_fields = ('entity',)


admin.site.register(models.History, HistoryAdmin)
