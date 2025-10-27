from django.db import models
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    name = models.CharField(
        _('Name'),
        max_length=100,
        unique=True,
        blank=False
    )
    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Label')
        verbose_name_plural = _('Labels')
        ordering = ['created_at']