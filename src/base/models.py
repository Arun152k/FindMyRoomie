from email.policy import default
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from django_countries.fields import CountryField


from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager
from .utils import check_ncsu_email


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField("email address", unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        email = self.email

        if not check_ncsu_email(email):
            raise ValueError("Please use NCSU Email Id!")
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.email


class Profile(models.Model):
    """Model for User Profile"""

    GENDER_MALE = "M"
    GENDER_FEMALE = "F"
    GENDER_OTHER = "O"

    DEGREE_BS = "B"
    DEGREE_MS = "M"
    DEGREE_PHD = "P"

    DIET_VEG = "V"
    DIET_NON_VEG = "NV"

    COURSE_CS = "CS"
    COURSE_CE = "CE"
    COURSE_EE = "EE"
    COURSE_MEC = "MEC"

    BLANK = "--"
    NO_PREF = "N/A"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    DEGREE_CHOICES = (
        (DEGREE_BS, "Bachelors Program (BS)"),
        (DEGREE_MS, "Masters Program (MS)"),
        (DEGREE_PHD, "Post Docterate (PHD)"),
    )

    COURSE_CHOICES = (
        (COURSE_CS, "Computer Science"),
        (COURSE_CE, "Computer Engg."),
        (COURSE_EE, "Electrical Engg."),
        (COURSE_MEC, "Mechanical Engg."),
    )

    DIET_CHOICES = ((DIET_VEG, "Veg"), (DIET_NON_VEG, "Non Veg"))

    PREF_GENDER_CHOICES = (
        (NO_PREF, "No Preference"),
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    PREF_DEGREE_CHOICES = (
        (NO_PREF, "No Preference"),
        (DEGREE_BS, "Bachelors Program (BS)"),
        (DEGREE_MS, "Masters Program (MS)"),
        (DEGREE_PHD, "Post Docterate (PHD)"),
    )

    PREF_DIET_CHOICES = (
        (NO_PREF, "No Preference"),
        (DIET_VEG, "Veg"),
        (DIET_NON_VEG, "Non Veg"),
    )

    PREF_COURSE_CHOICES = (
        (NO_PREF, "No Preference"),
        (COURSE_CS, "Computer Science"),
        (COURSE_CE, "Computer Engg."),
        (COURSE_EE, "Electrical Engg."),
        (COURSE_MEC, "Mechanical Engg."),
    )

    """User Profile Model"""
    name = models.CharField(max_length=100, default="")
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    hometown = models.CharField(max_length=100, default="", blank=True)

    gender = models.CharField(max_length=5, choices=GENDER_CHOICES, blank=True)
    degree = models.CharField(max_length=5, choices=DEGREE_CHOICES, blank=True)
    diet = models.CharField(max_length=5, choices=DIET_CHOICES, blank=True)
    country = CountryField(blank_label="Select Country", blank=True)
    course = models.CharField(max_length=5, choices=COURSE_CHOICES, blank=True)

    visibility = models.BooleanField(default=True)
    is_profile_complete = models.BooleanField(default=False)

    # preferences

    preference_gender = models.CharField(
        max_length=5, choices=PREF_GENDER_CHOICES, default=NO_PREF
    )
    preference_degree = models.CharField(
        max_length=5, choices=PREF_DEGREE_CHOICES, default=NO_PREF
    )
    preference_diet = models.CharField(
        max_length=5, choices=PREF_DIET_CHOICES, default=NO_PREF
    )
    preference_country = CountryField(
        blank_label="No Preference", blank=True, default="No Preference"
    )
    preference_course = models.CharField(
        max_length=5, choices=PREF_COURSE_CHOICES, default=NO_PREF
    )

    def __str__(self):
        return f"{self.user.email}-profile"


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    """Create User Profile"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    """Save User Profile"""
    instance.profile.save()
