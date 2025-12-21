from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User


# ======= სპორტი =======
class Sport(models.Model):
    #სპორტის ტიპები: BOX, MMA, BJJ ...

    name = models.CharField(max_length=100, unique=True, verbose_name='სახელი')
    description = models.TextField(blank=True, verbose_name='აღწერა')
    image = models.ImageField(upload_to='sports/', null=True, blank=True, verbose_name='სურათი')
    is_active = models.BooleanField(default=True, verbose_name='აქტიური')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'სპორტი'
        verbose_name_plural = 'სპორტები'
        ordering = ['name']

    def __str__(self):
        return self.name


class Training(models.Model):

    DIFFICULTY_CHOICES = [
        ('beginner', 'დამწყები'),
        ('intermediate', 'საშუალო'),
        ('advanced', 'მოწინავე'),
    ]


    sport = models.ForeignKey(
        Sport,
        # თუ სპორტი წაიშლება, ყგლეა სპორტული აქტივობა წაიშლოს
        on_delete=models.CASCADE,
        related_name='trainings',
        verbose_name='სპორტი'
    )
    coach = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role__in': ['admin', 'coach']},
        related_name='trainings',
        verbose_name='მწვრთნელი'
    )


    title = models.CharField(max_length=200, verbose_name='სათაური')
    description = models.TextField(blank=True, verbose_name='აღწერა')
    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default='beginner',
        verbose_name='სირთულე'
    )

    date = models.DateField(verbose_name='თარიღი')
    start_time = models.TimeField(verbose_name='დაწყების დრო')
    duration = models.IntegerField(
        validators=[MinValueValidator(15), MaxValueValidator(300)],
        help_text='წუთებში',
        verbose_name='ხანგრძლივობა'
    )

    max_participants = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(50)],
        default=20,
        verbose_name='მაქსიმალური მონაწილეები'
    )

    is_active = models.BooleanField(default=True, verbose_name='აქტიური')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'ვარჯიში'
        verbose_name_plural = 'ვარჯიშები'
        ordering = ['date', 'start_time']
        unique_together = ['coach', 'date','start_time']

    def __str__(self):
        return f"{self.title} - {self.date} {self.start_time}"

    @property
    def enrolled_count(self):
        #რეგისტრირებული ტრენერები
        return self.enrollments.filter(status='confirmed').count()

    @property
    def is_full(self):
        return self.enrolled_count >= self.max_participants

    @property
    def available_spots(self):
        return self.max_participants - self.enrolled_count

#ვარჯიშზე რეგისტრაცია
class Enrollment(models.Model):

    STATUS_CHOICES = [
        ('pending', 'მოლოდინში'),
        ('confirmed', 'დადასტურებული'),
        ('cancelled', 'გაუქმებული'),
        ('completed', 'დასრულებული'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='მომხმარებელი'
    )
    training = models.ForeignKey(
        Training,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='ვარჯიში'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='confirmed',
        verbose_name='სტატუსი'
    )
    attended = models.BooleanField(default=False, verbose_name='დაესწრო')
    notes = models.TextField(blank=True, verbose_name='შენიშვნები')
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name='ჩაწერის დრო')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'ჩაწერა'
        verbose_name_plural = 'ჩაწერები'
        ordering = ['-enrolled_at']
        unique_together = ['user', 'training']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.training.title}"


# ======= საწევროს პაკეტი =======
class MembershipPlan(models.Model):
    """საწევროს პაკეტები (ბრინჯაო, ვერცხლი, ოქრო)"""

    name = models.CharField(max_length=50, unique=True, verbose_name='სახელი')
    description = models.TextField(blank=True, verbose_name='აღწერა')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='ფასი'
    )
    duration_days = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text='რამდენი დღით',
        verbose_name='ხანგრძლივობა'
    )
    max_trainings_per_week = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text='კვირაში რამდენ ვარჯიშზე',
        verbose_name='ვარჯიშები კვირაში'
    )
    is_active = models.BooleanField(default=True, verbose_name='აქტიური')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'საწევროს პაკეტი'
        verbose_name_plural = 'საწევროს პაკეტები'
        ordering = ['price']

    def __str__(self):
        return f"{self.name} - {self.price}₾"


#საწევრო
class Membership(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='memberships',
        verbose_name='მომხმარებელი'
    )
    plan = models.ForeignKey(
        MembershipPlan,
        on_delete=models.PROTECT,
        related_name='memberships',
        verbose_name='პაკეტი'
    )
    start_date = models.DateField(verbose_name='დაწყების თარიღი')
    end_date = models.DateField(verbose_name='დასრულების თარიღი')
    is_active = models.BooleanField(default=True, verbose_name='აქტიური')
    auto_renew = models.BooleanField(default=False, verbose_name='ავტომატური განახლება')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'საწევრო'
        verbose_name_plural = 'საწევროები'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.plan.name}"

    @property
    def is_expired(self):
        from django.utils import timezone
        return timezone.now().date() > self.end_date