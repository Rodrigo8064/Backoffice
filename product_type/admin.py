from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import ProductType


admin.site.register(ProductType, MPTTModelAdmin)
