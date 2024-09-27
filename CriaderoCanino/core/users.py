from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, name, password, phone, is_boss):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
        email=self.normalize_email(email),
        name=name,
        phone=phone,
        is_boss=is_boss
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    # Campos personalizados
    is_boss = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email' # cual va a ser la PK
    REQUIRED_FIELDS = ['name', 'phone']