from django.contrib.auth import get_user_model
from rest_framework import serializers

from one.users.models import User as UserType

User = get_user_model()


class UserSerializer(serializers.ModelSerializer[UserType]):
    class Meta:
        model = User
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }


class UserMinimalSerializer(serializers.ModelSerializer[UserType]):
    status_display = serializers.SerializerMethodField(method_name="get_status_display")
    company = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "status", "status_display", "company", "department", "position"]

    def get_fields(self):
        fields = super().get_fields()
        removed_fields = self.context.get("removed_field", [])
        for _field in removed_fields:
            if _field in fields:
                del fields[_field]
        return fields

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_company(self, obj):
        return obj.company.name

    def get_department(self, obj):
        return obj.department.name

    def get_position(self, obj):
        return obj.position.name
