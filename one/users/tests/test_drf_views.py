from unittest import TestCase

import pytest
from django.test import Client
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from one.users.api.views import UserViewSet
from one.users.models import User
from one.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestUserViewSet:
    @pytest.fixture
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def test_get_queryset(self, user: User, api_rf: APIRequestFactory):
        view = UserViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert user in view.get_queryset()

    def test_me(self, user: User, api_rf: APIRequestFactory):
        view = UserViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user

        view.request = request

        response = view.me(request)  # type: ignore

        assert response.data == {
            "username": user.username,
            "url": f"http://testserver/api/users/{user.username}/",
            "name": user.name,
        }


class TestUserFilterViewSet(TestCase):
    def setUp(self):
        self.client = Client()
        UserFactory.create_batch(50)
        self.custom_user = UserFactory(first_name="custom_user_w")

    def test_init_test(self):
        assert User.objects.count() == 51

    def test_response_data_structure(self):
        # without params
        response = self.client.get(reverse("api:user_filter"))
        assert response.status_code == 200

        expected_fields = ["first_name", "last_name", "status", "status_display"]
        assert list(response.data.get("data")[0].keys()) == expected_fields

        # with full infor
        response = self.client.get(f'{reverse("api:user_filter")}?option=1')
        assert response.status_code == 200

        expected_fields = ["first_name", "last_name", "status", "status_display", "company", "department", "position"]
        assert list(response.data.get("data")[0].keys()) == expected_fields

    def test_filter(self):
        # expected exist
        response = self.client.get(f'{reverse("api:user_filter")}?q=user_w')
        assert response.status_code == 200
        assert len(response.data.get("data")) == 1

        self.custom_user.delete()

        response = self.client.get(f'{reverse("api:user_filter")}?q=user_w')
        assert response.status_code == 200
        assert len(response.data.get("data")) == 0
