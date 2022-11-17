from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from uuid import uuid4

# Create your models here.
class CustomUserModelManager(BaseUserManager):
  use_in_migrations = True

  def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

  def create_user(self, email, password=None, **extra_fields):
    """
      Creates a custom user with the given fields
    """

    extra_fields.setdefault('is_staff', False)
    extra_fields.setdefault('is_superuser', False)
    return self._create_user(email, password, **extra_fields)

  
  def create_superuser(self, email, password, **extra_fields):
      extra_fields.setdefault('is_staff', True)
      extra_fields.setdefault('is_superuser', True)
      if extra_fields.get('is_staff') is not True:
          raise ValueError('Superuser must have is_staff=True.')
      if extra_fields.get('is_superuser') is not True:
          raise ValueError('Superuser must have is_superuser=True.')
      return self._create_user(email, password, **extra_fields)


class CustomUserModel(AbstractUser, PermissionsMixin):
  username = None
  user_id    = models.CharField(max_length = 32, default = uuid4, primary_key = True, editable = False)
  email     = models.EmailField(max_length = 100, unique = True, null = False, blank = False)

  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = []

  objects = CustomUserModelManager()

  class Meta:
    verbose_name = "Custom User"