from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile
from django.urls import reverse

# Create your tests here.

class UserModelTest(TestCase):

    def test_create_user(self):

        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123"
        )

        self.assertEqual(
            user.username,
            "testuser"
        )

        self.assertEqual(
            user.email,
            "test@example.com"
        )

class ProfileSignalTest(TestCase):

    def test_profile_created(self):

        user = User.objects.create_user(
            username="signaluser",
            password="password123"
        )

        self.assertTrue(
            Profile.objects.filter(
                user=user
            ).exists()
        )

class LoginTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="loginuser",
            password="password123"
        )

    def test_login_successful(self):

        response = self.client.login(
            username="loginuser",
            password="password123"
        )

        self.assertTrue(response)

class ProtectedRouteTest(TestCase):

    def test_dashboard_requires_login(self):

        response = self.client.get(
            reverse("dashboard")
        )

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('dashboard')}"
        )

class DashboardAccessTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="adminuser",
            password="password123",
            is_staff=True
        )

    def test_staff_can_access_dashboard(self):

        self.client.login(
            username="adminuser",
            password="password123"
        )

        response = self.client.get(
            reverse("dashboard"),
            follow=True
        )

        self.assertEqual(
            response.status_code,
            200
        )