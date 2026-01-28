from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class ProductType(MPTTModel):
    name = models.CharField(max_length=200, unique=True, db_index=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        ancestors = self.get_ancestors(include_self=True)

        return ' > '.join([anc.name for anc in ancestors])
