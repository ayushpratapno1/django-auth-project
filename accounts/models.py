from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    DIVISION_CHOICES = [
        ("Operations", "Operations"),
        ("Intelligence", "Intelligence"),
        ("Security", "Security"),
        ("Logistics", "Logistics"),
        ("Strategy", "Strategy"),
    ]

    RANK_CHOICES = [
        ("Recruit", "Recruit"),
        ("Associate", "Associate"),
        ("Soldier", "Soldier"),
        ("Caporegime", "Caporegime"),
        ("Underboss", "Underboss"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )

    bio = models.TextField(
        blank=True
    )

    division = models.CharField(
        max_length=100,
        choices=DIVISION_CHOICES,
        blank=True
    )

    specialty = models.CharField(
        max_length=100,
        blank=True
    )

    territory = models.CharField(
        max_length=100,
        blank=True
    )

    rank = models.CharField(
        max_length=100,
        choices=RANK_CHOICES,
        default="Recruit"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
    max_length=20,
    default="Active"
    )

    def __str__(self):
        return self.user.username
    
class Message(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_deleted = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}"