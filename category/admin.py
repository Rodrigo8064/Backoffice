from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Category, Family, Source

admin.site.register(Category, MPTTModelAdmin)


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('name', 'is_active')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('name', 'is_active')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')
