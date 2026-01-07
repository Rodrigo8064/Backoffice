from django.db import models


class History(models.Model):
    entidade = models.CharField()
    ficha = models.CharField()
    nova_tax = models.CharField()
