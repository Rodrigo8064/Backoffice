from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=200, unique=True, db_index=True)
    url = models.CharField(max_length=4, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.CharField(max_length=50, blank=True, null=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        ancestors = self.get_ancestors(include_self=True)

        return ' > '.join([anc.name for anc in ancestors])


class Source(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Atualizado em'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Fonte'
        verbose_name_plural = 'Fontes'
        ordering = ['name']


class Family(models.Model):
    name = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Atualizado em'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Familia'
        verbose_name_plural = 'Familias'
        ordering = ['name']
