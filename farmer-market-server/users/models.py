# users/models.py
import uuid

from core.models.date_stamped_model import DateStampedModel
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import EmailValidator
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create(
        self,
        email,
        first_name,
        last_name,
        phone_number,
        password,
        user_type,
        **extra_fields,
    ):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            user_type=user_type,
            **extra_fields,
        )
        user.set_password(password)
        user.status = "Active"
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create(
            email, password=password, user_type="Superuser", **extra_fields
        )


class UserType(models.TextChoices):
    FARMER = "Farmer", "Farmer"
    BUYER = "Buyer", "Buyer"
    ADMINISTRATOR = "Administrator", "Administrator"
    SUPERUSER = "Superuser", "Superuser"


class Status(models.TextChoices):
    ACTIVE = "Active", "Active"
    INACTIVE = "Inactive", "Inactive"


class User(AbstractBaseUser, PermissionsMixin, DateStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    first_name = models.CharField(max_length=30, verbose_name="First Name")
    last_name = models.CharField(max_length=30, verbose_name="Last Name")
    email = models.EmailField(
        unique=True,
        verbose_name="Email Address",
        validators=[EmailValidator("Invalid email address")],
    )
    phone_number = models.CharField(
        max_length=15, verbose_name="Phone Number", validators=[]
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="Status",
    )
    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        null=False,
        blank=False,
        default=UserType.BUYER,
        verbose_name="User Type",
    )

    # Required fields for Django
    is_staff = models.BooleanField(default=False, verbose_name="Staff Status")
    is_active = models.BooleanField(default=True, verbose_name="Active Status")

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.email} ({self.user_type})"


class BuyerManager(UserManager):

    def create(
        self,
        email,
        first_name,
        last_name,
        phone_number,
        password,
        **extra_fields,
    ):
        return super().create(
            email,
            first_name,
            last_name,
            phone_number,
            password,
            user_type="Buyer",
            **extra_fields,
        )

    def get_queryset(self):
        return super().get_queryset().filter(user_type="Buyer")


class FarmerManager(UserManager):

    def create(
        self,
        email,
        first_name,
        last_name,
        phone_number,
        password,
        **extra_fields,
    ):
        return super().create(
            email,
            first_name,
            last_name,
            phone_number,
            password,
            user_type="Farmer",
            **extra_fields,
        )

    def get_queryset(self):
        return super().get_queryset().filter(user_type="Farmer")


class AdministratorManager(UserManager):

    def create(
        self,
        email,
        first_name,
        last_name,
        phone_number,
        password,
        **extra_fields,
    ):
        return super().create(
            email,
            first_name,
            last_name,
            phone_number,
            password,
            user_type="Administrator",
            is_staff=True,
            **extra_fields,
        )

    def get_queryset(self):
        return super().get_queryset().filter(user_type="Administrator")


class Buyer(User):
    objects = BuyerManager()

    class Meta:
        proxy = True
        verbose_name = "Buyer"
        verbose_name_plural = "Buyers"


class Farmer(User):
    objects = FarmerManager()

    class Meta:
        proxy = True
        verbose_name = "Farmer"
        verbose_name_plural = "Farmers"


class Administrator(User):
    objects = AdministratorManager()

    class Meta:
        proxy = True
        verbose_name = "Administrator"
        verbose_name_plural = "Administrators"
