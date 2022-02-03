from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from jsonfield import JSONField


class Roles(models.Model):
    role_id = models.IntegerField(
        verbose_name='user role identifyer',
        unique=True,
    )
    role_title = models.CharField(
        verbose_name='user role',
        max_length=24,
        unique=False,
    )
    is_admin = models.BooleanField(default=False)


class UserAccountManager(BaseUserManager):
    def create_user(self, c_addr, role_id, email=None, password=None, img_path=None):
        user = self.model(
            email=email,
            c_addr=c_addr,
            role_id=role_id,
            image = img_path
        )

        if password is None:
            password = "password123"

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, c_addr, email=None, password=None):
        
        if not email or email is None:
            raise ValueError('Must provide an email address')
            
        # admin default
        role_id = 1
        if password is None:
            password = "admin123"

        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            c_addr=c_addr,
            role_id=role_id
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=200,
        # NOTE:
        # Emails cannot be be unique since it is not required.
        # This means emails will be automatically set to NULL 
        # which consequently creates an error if unique.
        unique=False,
        null=True
    )
    c_addr = models.CharField(
        verbose_name='crypto address',
        max_length=42,
        unique=True,
    )
    image = models.CharField(
        verbose_name='user profile image',
        max_length=200,
        unique=False,
        null=True
    )
    claims = models.JSONField(
        verbose_name='references to userclaims',
        unique=False,
        null=True
    )
    role = models.ForeignKey(
        Roles,
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserAccountManager()

    USERNAME_FIELD = 'c_addr'
    # REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.c_addr

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin