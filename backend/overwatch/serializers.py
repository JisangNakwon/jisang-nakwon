from rest_framework import serializers
from .models import Streamer


class StreamerSerializer(serializers.ModelSerializer):
    mainPos  = serializers.CharField(source='main_pos')
    mainTier = serializers.CharField(source='main_tier')
    mainMost = serializers.JSONField(source='main_most')
    subPos   = serializers.CharField(source='sub_pos', allow_blank=True, default='')
    subTier  = serializers.CharField(source='sub_tier', allow_blank=True, default='')
    subMost  = serializers.JSONField(source='sub_most', default=list)

    class Meta:
        model  = Streamer
        fields = ['id', 'name', 'avatar', 'mainPos', 'mainTier', 'mainMost',
                  'subPos', 'subTier', 'subMost', 'note']
