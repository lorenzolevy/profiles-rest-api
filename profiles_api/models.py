from django.db import models

# Standard imports for extending base user classes
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings


# Make migrations to create DB tables for model

class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        # Error shown when email is not given
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        # Create hash of password
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user



# Extending of base user class
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    # Columns in DB
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    # Override default username to be email instead
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    # If function in class, self must be param
    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name
    
    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of our user"""
        return self.email



class ProfileFeedItem(models.Model):
    """Profile Status Update"""
    
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL, # from settings.py in project files
        on_delete = models.CASCADE, # delete user profile, and the feed item associated with CASCADE
    )
    status_text = models.CharField(max_length = 255) # like a tweet
    created_on = models.DateTimeField(auto_now_add = True) # Date/time of creation

    def __str__(self):
        """Return the model as a string"""
        return self.status_text