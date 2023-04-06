from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.urls import reverse

import pathlib
import uuid
# Create your models here.

class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        user_obj = self.model(
            email = self.normalize_email(email),
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj
    
    def create_staffuser(self, email, username, password):
        user = self.create_user(
            email,
            username,
            password=password,
            is_staff=True,

        )
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email,
            username,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        user.save(using=self._db)
        return user

def recipe_image_upload_handler(instance, filename):
    fpath = pathlib.Path(filename)
    new_fname = str(uuid.uuid1()) # uuid1 -> uuid + timestamps
    return f"accounts/images/{new_fname}{fpath.suffix}"

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    image = models.ImageField(upload_to=recipe_image_upload_handler, default='accounts/images/default.jpg')
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = AccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    def get_image_upload_url(self):
        return reverse("accounts:image-upload", kwargs={"id": self.id})
    
    def get_image(self):
        account_image = AccountImage.objects.filter(account__id=self.id).last()
        image = 'accounts/images/default.jpg'
        if account_image is not None:
            image =  account_image.image
        return f"https://django-delights.ams3.digitaloceanspaces.com/django-delights/mediafiles/{image}"
    
    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
    
class AccountImage(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=recipe_image_upload_handler, default='accounts/images/default.jpg')
