# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Models for the authentication app.
"""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

# MARK: Main Tables


class CustomAccountManager(BaseUserManager["UserModel"]):
    def create_superuser(
        self,
        email: str,
        username: str,
        password: str,
        **other_fields: bool,
    ) -> Any:
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")

        return self.create_user(
            email=email, username=username, password=password, **other_fields
        )

    def create_user(
        self,
        username: str,
        password: str,
        email: str = "",
        **other_fields: Any,
    ) -> UserModel:
        if email != "":
            email = self.normalize_email(email)

        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user


class SupportEntityType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Support(models.Model):
    supporter_type = models.ForeignKey(
        "SupportEntityType", on_delete=models.CASCADE, related_name="supporter"
    )
    supporter_entity = models.ForeignKey(
        "communities.Organization",
        on_delete=models.CASCADE,
        related_name="supporter",
    )
    supported_type = models.ForeignKey(
        "SupportEntityType", on_delete=models.CASCADE, related_name="supported"
    )
    supported_entity = models.ForeignKey(
        "communities.Organization",
        on_delete=models.CASCADE,
        related_name="supported",
    )
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.id)


class UserModel(AbstractUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True)
    password = models.CharField(max_length=255)
    location = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=500, blank=True)
    verified = models.BooleanField(default=False)
    verification_method = models.CharField(max_length=30, blank=True)
    verification_partner = models.ForeignKey(
        "authentication.UserModel", on_delete=models.SET_NULL, null=True
    )
    verification_code = models.UUIDField(blank=True, null=True)
    icon_url = models.ForeignKey(
        "content.Image", on_delete=models.SET_NULL, blank=True, null=True
    )
    email = models.EmailField(blank=True)
    is_confirmed = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    is_high_risk = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    # Django specific fields
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects: CustomAccountManager = CustomAccountManager()  # type: ignore

    USERNAME_FIELD = "username"

    resources = models.ManyToManyField("content.Resource", blank=True)
    social_links = models.ManyToManyField("content.SocialLink", blank=True)
    tasks = models.ManyToManyField("content.Task", blank=True)
    topics = models.ManyToManyField("content.Topic", blank=True)

    def __str__(self) -> str:
        return self.username
