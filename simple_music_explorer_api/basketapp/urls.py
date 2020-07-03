from rest_framework.routers import DefaultRouter

from basketapp.views import BasketViewSet

router = DefaultRouter()
router.register(r'', BasketViewSet, basename='basket')
urlpatterns = router.urls
