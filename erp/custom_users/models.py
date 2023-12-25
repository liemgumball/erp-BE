from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group, Permission
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom manager for the CustomUser model.
    """

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and return a superuser with the given email and password.

        @param {string} email - The email for the superuser.
        @param {string} password - The password for the superuser.
        @param {**extra_fields} - Additional fields for the superuser.
        @throws {ValueError} - If is_staff or is_superuser is not True.
        @returns {CustomUser} - The created superuser instance.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have `is_staff=True`.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have `is_superuser=True`.')

        return self.create_user(email, password, **extra_fields)

    def create_user(self, email, password, **extra_fields):
        """
        Create and return a regular user with the given email and password.

        @param {string} email - The email for the user.
        @param {string} password - The password for the user.
        @param {**extra_fields} - Additional fields for the user.
        @throws {ValueError} - If the email is not provided.
        @returns {CustomUser} - The created user instance.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))

        user = self.model(
            email=email,
            **extra_fields,
        )

        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that extends AbstractBaseUser and PermissionsMixin.
    """

    email = models.EmailField(_('email'), unique=True)
    name = models.CharField(max_length=50)
    phone = models.TextField(max_length=255, unique=True)
    avatar = models.URLField(max_length=500, blank=True)
    enroll_number = models.PositiveIntegerField(unique=True, default=1)


    created_at = models.DateTimeField(_('date joined'), auto_now_add=True)
    last_login = models.DateTimeField(_('last login'), auto_now=True)

    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff_status'), default=False)

    # Provide unique related_name arguments to avoid clashes
    groups = models.ManyToManyField(
        Group, related_name='custom_user_groups', blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name='custom_user_permissions', blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('User')

    def __str__(self):
        """
        String representation of the user object.

        @returns {string} - The email of the user.
        """
        return self.name if self.name else self.email


