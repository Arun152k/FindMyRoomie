from django.test import TestCase
from base.models import Profile
from django.contrib.auth import get_user_model


class TestModels(TestCase):
    def test_user_profile_model(self):
        user = get_user_model().objects.create_user(
            "admin@ncsu.edu", "password"
        )
        profile = Profile.objects.get(user=user)
        profile.name = "Arun"
        profile.bio = "Loving Life"
        profile.birth_date = "2000-11-15"
        profile.hometown = "Chennai"
        profile.gender = "Male"
        profile.degree = "Masters Program (MS)"
        profile.diet = "Non Veg"
        profile.country = "India"
        profile.visibility = "True"
        profile.preference_gender = "Male"
        profile.preference_country = "India"
        profile.preference_degree = "Masters Program (MS)"
        profile.preference_course = "Computer Science"
        profile.preference_diet = "Non Veg"
        profile.is_profile_complete = "True"
        profile.save()
        self.assertEqual(user.email, "admin@ncsu.edu")
        self.assertEqual(profile.name, "Arun")
        self.assertEqual(profile.bio, "Loving Life")
        self.assertEqual(profile.birth_date, "2000-11-15")
        self.assertEqual(profile.hometown, "Chennai")
        self.assertEqual(profile.gender, "Male")
        self.assertEqual(profile.degree, "Masters Program (MS)")
        self.assertEqual(profile.diet, "Non Veg")
        self.assertEqual(profile.country, "India")
        self.assertEqual(profile.visibility, "True")
        self.assertEqual(profile.preference_gender, "Male")
        self.assertEqual(profile.preference_country, "India")
        self.assertEqual(profile.preference_degree, "Masters Program (MS)")
        self.assertEqual(profile.preference_course, "Computer Science")
        self.assertEqual(profile.preference_diet, "Non Veg")
        self.assertEqual(profile.is_profile_complete, "True")
