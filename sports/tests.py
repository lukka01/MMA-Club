from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from datetime import date, time, timedelta
from .models import Sport, Training, Enrollment, MembershipPlan, Membership

User = get_user_model()


class SportModelTest(TestCase):

    def setUp(self):
        self.sport = Sport.objects.create(
            name='MMA',
            description='Mixed Martial Arts',
            is_active=True
        )

    def test_sport_creation(self):
        self.assertEqual(self.sport.name, 'MMA')
        self.assertTrue(self.sport.is_active)

    def test_sport_str_method(self):
        self.assertEqual(str(self.sport), 'MMA')


class TrainingModelTest(TestCase):

    def setUp(self):
        self.sport = Sport.objects.create(name='MMA')
        self.coach = User.objects.create_user(
            username='coach',
            email='coach@example.com',
            password='Pass123!',
            role='coach'
        )
        self.training = Training.objects.create(
            sport=self.sport,
            coach=self.coach,
            title='MMA Basics',
            difficulty='beginner',
            date=date.today() + timedelta(days=1),
            start_time=time(18, 0),
            duration=90,
            max_participants=15
        )

    def test_training_creation(self):
        self.assertEqual(self.training.title, 'MMA Basics')
        self.assertEqual(self.training.max_participants, 15)

    def test_training_enrolled_count(self):
        self.assertEqual(self.training.enrolled_count, 0)

        member = User.objects.create_user(
            username='member',
            email='member@example.com',
            password='Pass123!'
        )
        Enrollment.objects.create(
            user=member,
            training=self.training,
            status='confirmed'
        )
        self.assertEqual(self.training.enrolled_count, 1)

    def test_training_is_full(self):
        self.assertFalse(self.training.is_full)

        for i in range(15):
            member = User.objects.create_user(
                username=f'member{i}',
                email=f'member{i}@example.com',
                password='Pass123!'
            )
            Enrollment.objects.create(
                user=member,
                training=self.training,
                status='confirmed'
            )

        self.assertTrue(self.training.is_full)

    def test_training_available_spots(self):
        self.assertEqual(self.training.available_spots, 15)

        member = User.objects.create_user(
            username='member',
            email='member@example.com',
            password='Pass123!'
        )
        Enrollment.objects.create(
            user=member,
            training=self.training,
            status='confirmed'
        )

        self.assertEqual(self.training.available_spots, 14)


class EnrollmentModelTest(TestCase):

    def setUp(self):
        self.sport = Sport.objects.create(name='MMA')
        self.coach = User.objects.create_user(
            username='coach',
            email='coach@example.com',
            password='Pass123!',
            role='coach'
        )
        self.member = User.objects.create_user(
            username='member',
            email='member@example.com',
            password='Pass123!'
        )
        self.training = Training.objects.create(
            sport=self.sport,
            coach=self.coach,
            title='MMA Basics',
            date=date.today() + timedelta(days=1),
            start_time=time(18, 0),
            duration=90,
            max_participants=15
        )

    def test_enrollment_creation(self):
        enrollment = Enrollment.objects.create(
            user=self.member,
            training=self.training,
            status='confirmed'
        )
        self.assertEqual(enrollment.status, 'confirmed')
        self.assertFalse(enrollment.attended)

    def test_enrollment_unique_constraint(self):
        Enrollment.objects.create(
            user=self.member,
            training=self.training,
            status='confirmed'
        )

        with self.assertRaises(Exception):
            Enrollment.objects.create(
                user=self.member,
                training=self.training,
                status='confirmed'
            )


class MembershipPlanModelTest(TestCase):

    def test_membership_plan_creation(self):
        plan = MembershipPlan.objects.create(
            name='Bronze',
            price=100.00,
            duration_days=30,
            max_trainings_per_week=3
        )
        self.assertEqual(plan.name, 'Bronze')
        self.assertEqual(float(plan.price), 100.00)

    def test_membership_plan_str_method(self):
        plan = MembershipPlan.objects.create(
            name='Bronze',
            price=100.00,
            duration_days=30,
            max_trainings_per_week=3
        )
        self.assertEqual(str(plan), 'Bronze - 100.00₾')


class MembershipModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='member',
            email='member@example.com',
            password='Pass123!'
        )
        self.plan = MembershipPlan.objects.create(
            name='Bronze',
            price=100.00,
            duration_days=30,
            max_trainings_per_week=3
        )

    def test_membership_creation(self):
        membership = Membership.objects.create(
            user=self.user,
            plan=self.plan,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            is_active=True
        )
        self.assertTrue(membership.is_active)

    def test_membership_is_expired(self):
        membership = Membership.objects.create(
            user=self.user,
            plan=self.plan,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            is_active=True
        )
        self.assertFalse(membership.is_expired)

        expired_membership = Membership.objects.create(
            user=self.user,
            plan=self.plan,
            start_date=date.today() - timedelta(days=60),
            end_date=date.today() - timedelta(days=30),
            is_active=False
        )
        self.assertTrue(expired_membership.is_expired)


class SportAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='Pass123!',
            role='admin'
        )
        self.member = User.objects.create_user(
            username='member',
            email='member@example.com',
            password='Pass123!'
        )
        self.sport = Sport.objects.create(name='MMA', description='Mixed Martial Arts')
        self.list_url = reverse('sports:sport-list')

    def test_sport_list_authenticated(self):
        self.client.force_authenticate(user=self.member)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sport_create_admin(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            'name': 'BJJ',
            'description': 'Brazilian Jiu-Jitsu',
            'is_active': True
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_sport_create_member_forbidden(self):
        self.client.force_authenticate(user=self.member)
        data = {'name': 'BJJ', 'description': 'Brazilian Jiu-Jitsu'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
