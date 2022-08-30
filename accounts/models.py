from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, phone_number, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, phone number, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not phone_number:
            raise ValueError('Users must have a phone number')
        if not date_of_birth:
            raise ValueError('Users must have a date of birth')

        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            date_of_birth=date_of_birth,
        )

        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            phone_number=phone_number,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    phone_number = PhoneNumberField()
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth','phone_number']

    def __str__(self):
        return self.email

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

class Profile(models.Model):
    user = models.OneToOneField(MyUser, related_name='profile', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200,null=True,blank=False)
    last_name = models.CharField(max_length=200,null=True)
    online = models.BooleanField(default=False,blank=True)

    def __str__(self):
        if self.first_name != None:
            return f"{self.first_name}" 
        return f"{self.user}'s  profile"
