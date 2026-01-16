from django.db import models


class History(models.Model):
    entity = models.CharField()
    record = models.CharField()
    new_tax = models.CharField()

    def __str__(self):
        return self.entity

    class Meta:
        ordering = ['entity']
