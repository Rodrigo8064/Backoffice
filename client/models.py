from django.db import models


class DataClient(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    navigation = models.CharField()

    class Meta:
        ordering = ['-created_at']
