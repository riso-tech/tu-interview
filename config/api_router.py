from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from one.users.api.views import UserViewSet, user_filter

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)

app_name = "api"
urlpatterns = router.urls

urlpatterns += [path("test/user_filter/", user_filter, name="user_filter")]
