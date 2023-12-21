import time

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import UserMinimalSerializer, UserSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


def custom_ratelimit(num_requests, within_seconds):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            ip = request.META.get("REMOTE_ADDR")
            function_name = view_func.__name__

            cache_key = f"{function_name}_{ip}_requests"

            requests_cache = cache.get(cache_key, [])
            timestamp = time.time()

            if len(requests_cache) >= num_requests:
                last_requests = requests_cache[-num_requests:]

                time_diff = timestamp - last_requests[-1]["timestamp"]

                if time_diff < within_seconds:
                    requests_cache.append({"timestamp": timestamp, "status": "error"})
                    cache.set(cache_key, requests_cache)
                    return JsonResponse(
                        {"message": "Too many requests in a short period of time", "data": requests_cache}, status=429
                    )

            requests_cache.append({"timestamp": timestamp, "status": "success"})
            cache.set(cache_key, requests_cache)

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


@api_view()
@custom_ratelimit(num_requests=30, within_seconds=60)
def user_filter(request):
    has_param = False
    option = request.GET.get("option", None)
    removed_field = []
    if option != "1":
        removed_field = ["company", "department", "position"]

    qs = User.objects.filter()
    query_str = request.GET.get("q", None)
    if query_str:
        has_param = True
        qs = qs.filter(Q(first_name__icontains=query_str) | Q(last_name__icontains=query_str))

    status = request.GET.get("status", "").split(",")
    if status != [""]:
        has_param = True
        qs = qs.filter(status__in=status)

    company = request.GET.get("company", None)
    if company and "company" not in removed_field:
        has_param = True
        qs = qs.filter(company=company).select_related("company")

    department = request.GET.get("department", None)
    if department and "department" not in removed_field:
        has_param = True
        qs = qs.filter(department=department).select_related("department")

    position = request.GET.get("position", None)
    if position and "position" not in removed_field:
        has_param = True
        qs = qs.filter(position=position).select_related("position")

    if not has_param:
        if not removed_field:
            qs = User.objects.all().select_related("company", "department", "position")
        else:
            qs = User.objects.all()

    paginator = Paginator(qs, 1000)

    current_page_number = request.GET.get("page", 1)
    current_page = paginator.page(current_page_number)

    objects_on_page = current_page.object_list

    data = UserMinimalSerializer(objects_on_page, many=True, context={"removed_field": removed_field}).data

    return Response({"data": data}, status=200)
