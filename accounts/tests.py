import shutil
import tempfile
from datetime import timedelta

from django.contrib import admin
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .admin import MessageAdmin
from .forms import MissionForm, ProfileForm, SignUpForm
from .models import Message, Mission, Profile


TEST_MEDIA_ROOT = tempfile.mkdtemp(dir="C:\\tmp")
TEST_STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


@override_settings(SECURE_SSL_REDIRECT=False, MEDIA_ROOT=TEST_MEDIA_ROOT, STORAGES=TEST_STORAGES)
class BaseAccountsTestCase(TestCase):
    """Shared helpers for account, profile, operation, and chat tests."""

    password = "VeryStrongPass123!"

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)

    def create_user(self, username="member", password=None, **kwargs):
        return User.objects.create_user(
            username=username,
            email=kwargs.pop("email", f"{username}@example.com"),
            password=password or self.password,
            **kwargs,
        )

    def login_user(self, user, password=None):
        return self.client.login(
            username=user.username,
            password=password or self.password,
        )

    def set_rank(self, user, rank):
        user.profile.rank = rank
        user.profile.save(update_fields=["rank"])
        return user.profile

    def image_upload(self, name="avatar.gif"):
        # Small valid GIF used to exercise ImageField validation and saving.
        return SimpleUploadedFile(
            name,
            b"GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,"
            b"\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;",
            content_type="image/gif",
        )


class ModelTests(BaseAccountsTestCase):
    """Verify core model creation, default values, and string methods."""

    def test_profile_created_with_defaults_and_string_method(self):
        user = self.create_user("profileuser")

        self.assertTrue(Profile.objects.filter(user=user).exists())
        self.assertEqual(user.profile.rank, "Recruit")
        self.assertEqual(user.profile.status, "Active")
        self.assertEqual(user.profile.bio, "")
        self.assertEqual(str(user.profile), "profileuser")

    def test_mission_creation_defaults_and_string_method(self):
        user = self.create_user("missionowner")
        mission = Mission.objects.create(
            title="Night Watch",
            description="Monitor activity.",
            created_by=user,
        )

        self.assertEqual(mission.status, "Planning")
        self.assertEqual(mission.created_by, user)
        self.assertEqual(str(mission), "Night Watch")

    def test_message_creation_defaults_and_string_method(self):
        user = self.create_user("sender")
        message = Message.objects.create(
            user=user,
            content="This is a long secure communication message.",
        )

        self.assertFalse(message.is_deleted)
        self.assertEqual(
            str(message),
            "sender: This is a long secure communic",
        )


class SignalTests(BaseAccountsTestCase):
    """Signals should guarantee every newly registered user has a profile."""

    def test_profile_automatically_created_after_user_registration(self):
        user = self.create_user("signaluser")

        self.assertIsNotNone(user.profile)
        self.assertEqual(Profile.objects.filter(user=user).count(), 1)


class AuthenticationTests(BaseAccountsTestCase):
    """Cover signup, login, logout, and anonymous protected-route handling."""

    def setUp(self):
        self.user = self.create_user("loginuser")

    def test_signup_success_creates_user_and_redirects_home(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newmember",
                "first_name": "New",
                "last_name": "Member",
                "email": "newmember@example.com",
                "password1": self.password,
                "password2": self.password,
            },
        )

        self.assertRedirects(response, reverse("home"))
        self.assertTrue(User.objects.filter(username="newmember").exists())
        self.assertTrue(Profile.objects.filter(user__username="newmember").exists())

    def test_login_success_redirects_home_and_authenticates_session(self):
        response = self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": self.password},
        )

        self.assertRedirects(response, reverse("home"))
        self.assertEqual(
            int(self.client.session["_auth_user_id"]),
            self.user.pk,
        )

    def test_login_failure_stays_on_login_page(self):
        response = self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": "wrong-password"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout_clears_session_and_redirects_home(self):
        self.login_user(self.user)

        response = self.client.get(reverse("logout"))

        self.assertRedirects(response, reverse("home"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_protected_routes_redirect_anonymous_users_to_login(self):
        protected_routes = [
            reverse("profile"),
            reverse("edit_profile"),
            reverse("members"),
            reverse("chat"),
            reverse("chat_messages"),
            reverse("operations"),
            reverse("create_operation"),
            reverse("dashboard"),
            reverse("user_detail", args=[self.user.pk]),
        ]

        for route in protected_routes:
            with self.subTest(route=route):
                response = self.client.get(route)
                self.assertEqual(response.status_code, 302)
                self.assertIn(reverse("login"), response["Location"])


class ProfileTests(BaseAccountsTestCase):
    """Profile pages should render, update data, and accept image uploads."""

    def setUp(self):
        self.user = self.create_user("profilemember")
        self.login_user(self.user)

    def test_view_profile(self):
        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")
        self.assertContains(response, self.user.username)

    def test_edit_profile_page_loads(self):
        response = self.client.get(reverse("edit_profile"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_profile.html")

    def test_update_profile_data(self):
        response = self.client.post(
            reverse("edit_profile"),
            {
                "bio": "Operational strategist.",
                "division": "Strategy",
                "specialty": "Planning",
                "territory": "North Sector",
            },
        )

        self.assertRedirects(response, reverse("profile"))
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.bio, "Operational strategist.")
        self.assertEqual(self.user.profile.division, "Strategy")
        self.assertEqual(self.user.profile.specialty, "Planning")
        self.assertEqual(self.user.profile.territory, "North Sector")

    def test_upload_profile_image(self):
        response = self.client.post(
            reverse("edit_profile"),
            {
                "profile_picture": self.image_upload(),
                "bio": "Image upload test.",
                "division": "Security",
                "specialty": "Protection",
                "territory": "East Sector",
            },
        )

        self.assertRedirects(response, reverse("profile"))
        self.user.profile.refresh_from_db()
        self.assertTrue(self.user.profile.profile_picture.name)
        self.assertIn("profile_pictures/", self.user.profile.profile_picture.name)


class MembersDirectoryTests(BaseAccountsTestCase):
    """Members directory is available to authenticated users only."""

    def setUp(self):
        self.user = self.create_user("directoryuser")
        self.other_user = self.create_user("othermember")

    def test_authenticated_user_can_view_members(self):
        self.login_user(self.user)

        response = self.client.get(reverse("members"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "members.html")
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.other_user.username)

    def test_anonymous_user_blocked_from_members(self):
        response = self.client.get(reverse("members"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])


class OperationsTests(BaseAccountsTestCase):
    """Rank-based operation permissions and mission visibility."""

    def setUp(self):
        self.user = self.create_user("operator")
        self.admin_user = self.create_user("admin", is_staff=True)

    def test_operations_page_loads_for_authenticated_user(self):
        self.login_user(self.user)

        response = self.client.get(reverse("operations"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "operations.html")

    def test_mission_creation_and_visibility(self):
        mission = Mission.objects.create(
            title="Visible Mission",
            description="Visible to authenticated members.",
            created_by=self.admin_user,
            status="Active",
        )
        self.login_user(self.user)

        response = self.client.get(reverse("operations"))

        self.assertContains(response, mission.title)
        self.assertContains(response, mission.description)
        self.assertContains(response, mission.status)

    def assert_can_create_operation(self, user):
        self.login_user(user)
        response = self.client.post(
            reverse("create_operation"),
            {
                "title": f"Mission by {user.username}",
                "description": "Authorized operation.",
                "status": "Planning",
            },
        )

        self.assertRedirects(response, reverse("operations"))
        self.assertTrue(
            Mission.objects.filter(
                title=f"Mission by {user.username}",
                created_by=user,
            ).exists()
        )

    def assert_cannot_create_operation(self, user):
        self.login_user(user)
        response = self.client.post(
            reverse("create_operation"),
            {
                "title": f"Blocked mission by {user.username}",
                "description": "Unauthorized operation.",
                "status": "Active",
            },
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(
            Mission.objects.filter(title=f"Blocked mission by {user.username}").exists()
        )

    def test_caporegime_can_create_operations(self):
        self.set_rank(self.user, "Caporegime")
        self.assert_can_create_operation(self.user)

    def test_underboss_can_create_operations(self):
        self.set_rank(self.user, "Underboss")
        self.assert_can_create_operation(self.user)

    def test_admin_can_create_operations(self):
        self.assert_can_create_operation(self.admin_user)

    def test_recruit_cannot_create_operations(self):
        self.set_rank(self.user, "Recruit")
        self.assert_cannot_create_operation(self.user)

    def test_associate_cannot_create_operations(self):
        self.set_rank(self.user, "Associate")
        self.assert_cannot_create_operation(self.user)

    def test_soldier_cannot_create_operations(self):
        self.set_rank(self.user, "Soldier")
        self.assert_cannot_create_operation(self.user)


class CommunicationCenterTests(BaseAccountsTestCase):
    """Chat views, AJAX endpoints, persistence, and last-100-message limit."""

    def setUp(self):
        self.user = self.create_user("chatuser")
        self.login_user(self.user)

    def test_chat_page_loads(self):
        response = self.client.get(reverse("chat"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chat.html")

    def test_send_message_saves_message_to_database(self):
        response = self.client.post(
            reverse("send_message"),
            {"content": "Secure hello."},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": True})
        self.assertTrue(
            Message.objects.filter(user=self.user, content="Secure hello.").exists()
        )

    def test_ajax_message_loading_returns_json(self):
        Message.objects.create(user=self.user, content="Loaded by AJAX.")

        response = self.client.get(
            reverse("chat_messages"),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        payload = response.json()
        self.assertIn("messages", payload)
        self.assertEqual(payload["messages"][0]["user"], self.user.username)
        self.assertEqual(payload["messages"][0]["content"], "Loaded by AJAX.")

    def test_send_message_ignores_empty_string_but_returns_success(self):
        response = self.client.post(reverse("send_message"), {"content": ""})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": True})
        self.assertEqual(Message.objects.count(), 0)

    def test_deleted_messages_are_not_displayed_or_returned(self):
        Message.objects.create(user=self.user, content="Visible message.")
        Message.objects.create(user=self.user, content="Hidden message.", is_deleted=True)

        page_response = self.client.get(reverse("chat"))
        ajax_response = self.client.get(reverse("chat_messages"))

        self.assertContains(page_response, "Visible message.")
        self.assertNotContains(page_response, "Hidden message.")
        contents = [item["content"] for item in ajax_response.json()["messages"]]
        self.assertEqual(contents, ["Visible message."])

    def test_last_100_messages_limit_uses_latest_non_deleted_messages(self):
        base_time = timezone.now()
        for index in range(105):
            message = Message.objects.create(
                user=self.user,
                content=f"message-{index}",
            )
            Message.objects.filter(pk=message.pk).update(
                created_at=base_time + timedelta(seconds=index)
            )

        response = self.client.get(reverse("chat_messages"))
        contents = [item["content"] for item in response.json()["messages"]]

        self.assertEqual(len(contents), 100)
        self.assertEqual(contents[0], "message-5")
        self.assertEqual(contents[-1], "message-104")
        self.assertNotIn("message-0", contents)
        self.assertNotIn("message-4", contents)


class AdminDashboardTests(BaseAccountsTestCase):
    """Staff-only dashboard and user detail permissions."""

    def setUp(self):
        self.staff_user = self.create_user("staffuser", is_staff=True)
        self.member_user = self.create_user("regularuser")

    def test_staff_can_access_dashboard_with_statistics(self):
        self.login_user(self.staff_user)

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard.html")
        self.assertContains(response, "Registered Users")
        self.assertEqual(response.context["total_users"], 2)
        self.assertEqual(response.context["staff_users"], 1)
        self.assertEqual(response.context["total_profiles"], 2)

    def test_non_staff_denied_dashboard(self):
        self.login_user(self.member_user)

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 403)

    def test_staff_can_access_user_detail_page(self):
        self.login_user(self.staff_user)

        response = self.client.get(reverse("user_detail", args=[self.member_user.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user_detail.html")
        self.assertContains(response, self.member_user.username)

    def test_non_staff_denied_user_detail_page(self):
        self.login_user(self.member_user)

        response = self.client.get(reverse("user_detail", args=[self.staff_user.pk]))

        self.assertEqual(response.status_code, 403)


class AdminModerationTests(BaseAccountsTestCase):
    """Admin registration exposes Message moderation fields and filters."""

    def test_message_model_is_registered_for_admin_moderation(self):
        self.assertIn(Message, admin.site._registry)
        self.assertIsInstance(admin.site._registry[Message], MessageAdmin)

    def test_message_admin_exposes_deletion_moderation_controls(self):
        message_admin = admin.site._registry[Message]

        self.assertIn("is_deleted", message_admin.list_display)
        self.assertIn("is_deleted", message_admin.list_filter)
        self.assertIn("content", message_admin.search_fields)


class URLTests(BaseAccountsTestCase):
    """Major routes should return the expected status for each access level."""

    def setUp(self):
        self.user = self.create_user("urluser")
        self.staff_user = self.create_user("urlstaff", is_staff=True)

    def test_public_routes_return_success_for_anonymous_users(self):
        for name in ["home", "signup", "login"]:
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)

    def test_authenticated_member_routes_return_success(self):
        self.login_user(self.user)
        for name in ["profile", "edit_profile", "members", "chat", "chat_messages", "operations"]:
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)

    def test_create_operation_route_status_by_permission(self):
        self.login_user(self.user)
        response = self.client.get(reverse("create_operation"))
        self.assertEqual(response.status_code, 403)

        self.client.logout()
        self.set_rank(self.user, "Underboss")
        self.login_user(self.user)
        response = self.client.get(reverse("create_operation"))
        self.assertEqual(response.status_code, 200)

    def test_staff_routes_return_success_for_staff(self):
        self.login_user(self.staff_user)
        for route in [reverse("dashboard"), reverse("user_detail", args=[self.user.pk])]:
            with self.subTest(route=route):
                response = self.client.get(route)
                self.assertEqual(response.status_code, 200)


class FormTests(BaseAccountsTestCase):
    """Validate production forms independently from their views."""

    def test_signup_form_validates_required_user_data(self):
        form = SignUpForm(
            data={
                "username": "formuser",
                "first_name": "Form",
                "last_name": "User",
                "email": "formuser@example.com",
                "password1": self.password,
                "password2": self.password,
            }
        )

        self.assertTrue(form.is_valid(), form.errors)

    def test_signup_form_rejects_password_mismatch(self):
        form = SignUpForm(
            data={
                "username": "badformuser",
                "first_name": "Bad",
                "last_name": "User",
                "email": "badformuser@example.com",
                "password1": self.password,
                "password2": "DifferentPass123!",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_profile_form_validation_accepts_profile_fields(self):
        form = ProfileForm(
            data={
                "bio": "Validated profile.",
                "division": "Intelligence",
                "specialty": "Research",
                "territory": "West Sector",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)

    def test_profile_form_rejects_invalid_division_choice(self):
        form = ProfileForm(
            data={
                "bio": "Invalid profile.",
                "division": "Unknown Division",
                "specialty": "Research",
                "territory": "West Sector",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("division", form.errors)

    def test_mission_form_validation_accepts_valid_mission(self):
        form = MissionForm(
            data={
                "title": "Form Mission",
                "description": "A valid operation.",
                "status": "Active",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)

    def test_mission_form_rejects_missing_title(self):
        form = MissionForm(
            data={
                "title": "",
                "description": "Missing a title.",
                "status": "Planning",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)