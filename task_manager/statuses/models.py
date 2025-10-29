from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
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
        verbose_name = _('Status')
        verbose_name_plural = _('Statuses')
        ordering = ['created_at']