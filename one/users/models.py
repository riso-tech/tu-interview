from django.contrib.auth.models import AbstractUser
from django.db.models import CASCADE, CharField, ForeignKey, Model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Company(Model):
    name = CharField("Company Name", max_length=150)


class Department(Model):
    name = CharField("Department Name", max_length=150)
    company = ForeignKey(Company, on_delete=CASCADE)


class Position(Model):
    name = CharField("Position Name", max_length=150)
    department = ForeignKey(Department, on_delete=CASCADE)


class User(AbstractUser):
    """
    Default custom user model for Django Software as a Service.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    STATUS_ACTIVE = 2
    STATUS_INACTIVE = 1
    STATUS_TERMINATED = 0
    STATUS_CHOICES = ((STATUS_ACTIVE, "Active"), (STATUS_INACTIVE, "Not Started"), (STATUS_TERMINATED, "Terminated"))

    status = CharField(_("Status"), max_length=10, choices=STATUS_CHOICES, default=STATUS_INACTIVE)

    company = ForeignKey(Company, on_delete=CASCADE, null=True, blank=True)
    department = ForeignKey(Department, on_delete=CASCADE, null=True, blank=True)
    position = ForeignKey(Position, on_delete=CASCADE, null=True, blank=True)

    name = CharField(_("Full Name"), max_length=250, null=True, blank=True)

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def get_status_display(self) -> str:
        return dict(self.STATUS_CHOICES).get(int(self.status), self.status)
