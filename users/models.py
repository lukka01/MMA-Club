from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import secrets


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'ადმინისტრატორი'),
        ('coach','მწვრთნელი'),
        ('member', 'წევრი'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='member'
    )

    phone = models.CharField(max_length=15, blank=True, verbose_name="ტელეფონი")
    birth_date = models.DateField(null=True,blank=True,verbose_name="დაბადების თარიღი")
    address = models.TextField(blank=True,verbose_name="მისამართი ")

    profile_image = models.ImageField(
        upload_to='profiles/',
        null=True,
        blank= True,
        verbose_name = "პროფილის ფოტო"
    )

    membership_start = models.DateField(auto_now_add= True)
    is_active_member = models.BooleanField(default= True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "წევრი",
        verbose_name_plural = "წევრები"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_full_name()}  ({self.get_role_display()})"

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.username

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_coach(self):
        return self.role == 'coach'

    @property
    def is_member(self):
        return self.role == 'member'

#პაროლის აღდგენის შესაძლებლობა
class PasswordResetToken(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reset_tokens',
        verbose_name = 'მომხმარებელი'
    )

    token = models.CharField(max_length=100, unique=True, verbose_name='ტოკენი')
    created_at = models.DateTimeField(auto_now_add=True)

    is_used = models.BooleanField(default=False, verbose_name='გამოყენებული')
    expires_at = models.DateTimeField(verbose_name='ვადის გასვლა')


    class Meta:
        verbose_name = 'პაროლის აღდგენის ტოკენი'
        verbose_name_plural = 'პაროლის აღდგენის ტოკენები'
        ordering = ['-created_at']


    def __str__(self):
        return f"Reset token for {self.user.username}"


    @classmethod
    def create_token(cls, user):
        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timezone.timedelta(hours=1)
        return cls.objects.create(user=user, token=token, expires_at=expires_at)


    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at

    #tu gamoyenebulia monishnavs
    def mark_as_used(self):
        self.is_used = True
        self.save()
