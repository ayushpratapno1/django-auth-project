from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Profile


class BaseTestCase(TestCase):
    """Base class providing helper methods for all test cases."""

    def create_user(
        self,
        username,
        password="password123",
        email=None,
        is_staff=False,
    ):
        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=is_staff,
        )


class UserModelTest(BaseTestCase):

    def test_create_user(self):

        user = self.create_user(
            username="testuser",
            email="test@example.com",
        )

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")


class ProfileSignalTest(BaseTestCase):

    def test_profile_created(self):

        user = self.create_user("signaluser")

        self.assertEqual(
            Profile.objects.filter(user=user).count(),
            1,
        )


class LoginTest(BaseTestCase):

    def setUp(self):

        self.create_user("loginuser")

    def test_login_successful(self):

        self.assertTrue(

            self.client.login(
                username="loginuser",
                password="password123",
            )

        )


class LoginFailureTest(BaseTestCase):

    def setUp(self):

        self.create_user("testuser")

    def test_login_failed(self):

        response = self.client.post(

            reverse("login"),

            {
                "username": "testuser",
                "password": "wrongpassword",
            }

        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertNotIn(
            "_auth_user_id",
            self.client.session,
        )


class LogoutTest(BaseTestCase):

    def setUp(self):

        self.create_user("logoutuser")

    def test_logout(self):

        self.client.login(
            username="logoutuser",
            password="password123",
        )

        response = self.client.get(
            reverse("logout")
        )

        self.assertRedirects(
            response,
            reverse("home"),
        )

        self.assertNotIn(
            "_auth_user_id",
            self.client.session,
        )


class SignupTest(BaseTestCase):

    def test_signup(self):

        response = self.client.post(

            reverse("signup"),

            {
                "username": "newuser",
                "first_name": "New",
                "last_name": "User",
                "email": "new@example.com",
                "password1": "StrongPassword123",
                "password2": "StrongPassword123",
            }

        )

        self.assertRedirects(
            response,
            reverse("home"),
        )

        self.assertTrue(

            User.objects.filter(
                username="newuser"
            ).exists()

        )


class SignupSignalTest(BaseTestCase):

    def test_profile_created_after_signup(self):

        self.client.post(

            reverse("signup"),

            {
                "username": "signaltest",
                "first_name": "Signal",
                "last_name": "Test",
                "email": "signal@test.com",
                "password1": "StrongPassword123",
                "password2": "StrongPassword123",
            }

        )

        user = User.objects.get(
            username="signaltest"
        )

        self.assertEqual(
            Profile.objects.filter(user=user).count(),
            1,
        )


class HomePageTest(BaseTestCase):

    def test_home_page(self):

        response = self.client.get(
            reverse("home")
        )

        self.assertEqual(
            response.status_code,
            200,
        )


class ProtectedRouteTest(BaseTestCase):

    def test_dashboard_requires_login(self):

        response = self.client.get(
            reverse("dashboard"),
            follow=True,
        )

        self.assertContains(
            response,
            "Login",
        )


class ProfileViewTest(BaseTestCase):

    def setUp(self):

        self.create_user("profileuser")

    def test_profile_page(self):

        self.client.login(
            username="profileuser",
            password="password123",
        )

        response = self.client.get(
            reverse("profile")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            "profileuser",
        )


class EditProfileTest(BaseTestCase):

    def setUp(self):

        self.create_user("edituser")

    def test_edit_profile_page(self):

        self.client.login(
            username="edituser",
            password="password123",
        )

        response = self.client.get(
            reverse("edit_profile")
        )

        self.assertEqual(
            response.status_code,
            200,
        )


class UpdateProfileTest(BaseTestCase):

    def setUp(self):

        self.user = self.create_user("updateuser")

    def test_update_profile(self):

        self.client.login(
            username="updateuser",
            password="password123",
        )

        response = self.client.post(

            reverse("edit_profile"),

            {
                "bio": "Backend Developer",
                "github": "https://github.com/test",
                "linkedin": "https://linkedin.com/in/test",
            }

        )

        self.assertRedirects(
            response,
            reverse("profile"),
        )

        self.user.profile.refresh_from_db()

        self.assertEqual(
            self.user.profile.bio,
            "Backend Developer",
        )


class DashboardAccessTest(BaseTestCase):

    def setUp(self):

        self.create_user(
            username="adminuser",
            is_staff=True,
        )

    def test_staff_can_access_dashboard(self):

        self.client.login(
            username="adminuser",
            password="password123",
        )

        response = self.client.get(
            reverse("dashboard"),
            follow=True,
        )

        self.assertEqual(
            response.status_code,
            200,
        )


class NonStaffDashboardTest(BaseTestCase):

    def setUp(self):

        self.create_user("member")

    def test_non_staff_dashboard(self):

        self.client.login(
            username="member",
            password="password123",
        )

        response = self.client.get(
            reverse("dashboard")
        )

        self.assertEqual(
            response.status_code,
            403,
        )


class UserDetailTest(BaseTestCase):

    def setUp(self):

        self.staff = self.create_user(
            username="admin",
            is_staff=True,
        )

        self.member = self.create_user(
            username="member",
        )

    def test_user_detail(self):

        self.client.login(
            username="admin",
            password="password123",
        )

        response = self.client.get(

            reverse(
                "user_detail",
                args=[self.member.id],
            )

        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            "member",
        )