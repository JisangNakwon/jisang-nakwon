from django.db import models


class Streamer(models.Model):
    name      = models.CharField(max_length=100, unique=True)
    avatar    = models.CharField(max_length=10, default='🎮')
    main_pos  = models.CharField(max_length=20)
    main_tier = models.CharField(max_length=10)
    main_most = models.JSONField(default=list)
    sub_pos   = models.CharField(max_length=20, blank=True, default='')
    sub_tier  = models.CharField(max_length=10, blank=True, default='')
    sub_most  = models.JSONField(default=list)
    note      = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
