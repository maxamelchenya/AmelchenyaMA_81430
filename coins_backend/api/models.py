from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("username"), max_length=255)
    email = models.EmailField(_("email"), unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(_("avatar"), upload_to="avatars", null=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_superuser = models.BooleanField(_("superuser status"), default=False)
    is_active = models.BooleanField(_("active status"), default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(_("name"), max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(_("name"), max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "countries"

    def __str__(self):
        return self.name


def default_end_date():
    return timezone.now() + timezone.timedelta(days=10)


class Coin(models.Model):
    STATUS_CHOICES = (
        (_("Pending"), _("Pending")),
        (_("For sale"), _("For sale")),
        (_("Sold"), _("Sold")),
        (_("Off-sale"), _("Off-sale")),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=255, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0]
    )
    name = models.CharField(_("name"), max_length=255)
    image = models.ImageField(_("image"), upload_to="coins", null=True)
    description = models.TextField(
        _("description"),
    )
    price = models.DecimalField(_("price"), max_digits=8, decimal_places=2)
    year = models.PositiveSmallIntegerField(
        _("year"),
    )
    end_date = models.DateTimeField(_("end date"), default=default_end_date)

    def __str__(self):
        return self.name


class BidHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    price = models.DecimalField(_("price"), max_digits=8, decimal_places=2)
    date = models.DateTimeField(_("date"), default=timezone.now)

    class Meta:
        verbose_name_plural = "bid history"

    def __str__(self):
        return f"{self.user}, {self.coin}"
