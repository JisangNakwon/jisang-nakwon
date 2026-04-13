from django.contrib import admin
from .models import Streamer

@admin.register(Streamer)
class StreamerAdmin(admin.ModelAdmin):
    list_display = ['name', 'main_pos', 'main_tier', 'sub_pos', 'sub_tier']
    ordering     = ['name']
