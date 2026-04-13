from rest_framework import viewsets, permissions
from .models import Streamer
from .serializers import StreamerSerializer


class StreamerViewSet(viewsets.ModelViewSet):
    queryset           = Streamer.objects.all()
    serializer_class   = StreamerSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
