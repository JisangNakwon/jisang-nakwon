from rest_framework.routers import DefaultRouter
from .views import StreamerViewSet

router = DefaultRouter()
router.register(r'streamers', StreamerViewSet)

urlpatterns = router.urls
