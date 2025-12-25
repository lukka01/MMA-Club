"""
sports/tests.py - Sports App Test Cases
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from datetime import date, time, timedelta
from .models import Sport, Training, Enrollment, MembershipPlan, Membership

User = get_user_model()

#ტესტები

class SportModelTest(TestCase):
    """Sport Model Tests"""

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
        """Test training creation"""
        self.assertEqual(self.training.title, 'MMA Basics')
        self.assertEqual(self.training.max_participants, 15)

    def test_training_enrolled_count(self):
        """Test enrolled count property"""
        self.assertEqual(self.training.enrolled_count, 0)

        # Create enrollment
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
        """Test is_full property"""
        self.assertFalse(self.training.is_full)

        # Fill up the training
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
        """Test available spots property"""
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
    """Enrollment Model Tests"""

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
        """Test membership plan string representation"""
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
        #აქტიური წევრი
        membership = Membership.objects.create(
            user=self.user,
            plan=self.plan,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            is_active=True
        )
        self.assertFalse(membership.is_expired)

        # Expired membership
        expired_membership = Membership.objects.create(
            user=self.user,
            plan=self.plan,
            start_date=date.today() - timedelta(days=60),
            end_date=date.today() - timedelta(days=30),
            is_active=False
        )
        self.assertTrue(expired_membership.is_expired)


# ==================== API TESTS ====================

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


class TrainingAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()
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
            difficulty='beginner',
            date=date.today() + timedelta(days=1),
            start_time=time(18, 0),
            duration=90,
            max_participants=15
        )
        self.list_url = reverse('sports:training-list')

    def test_training_list(self):
        self.client.force_authenticate(user=self.member)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_training_create_coach(self):
        self.client.force_authenticate(user=self.coach)
        data = {
            'sport': self.sport.id,
            'title': 'Advanced MMA',
            'difficulty': 'advanced',
            'date': str(date.today() + timedelta(days=2)),
            'start_time': '19:00',
            'duration': 90,
            'max_participants': 10
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_training_create_member_forbidden(self):
        """Test training creation forbidden for members"""
        self.client.force_authenticate(user=self.member)
        data = {
            'sport': self.sport.id,
            'title': 'Test Training',
            'date': str(date.today() + timedelta(days=1)),
            'start_time': '18:00',
            'duration': 90,
            'max_participants': 15
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_training_filter_by_sport(self):
        """Test training filtering by sport"""
        self.client.force_authenticate(user=self.member)
        response = self.client.get(f"{self.list_url}?sport={self.sport.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class EnrollmentAPITest(APITestCase):
    """Enrollment API Tests"""

    def setUp(self):
        self.client = APIClient()
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
            max_participants=2
        )

    def test_enroll_success(self):
        self.client.force_authenticate(user=self.member)
        enroll_url = reverse('sports:training-enroll', kwargs={'training_id': self.training.id})
        response = self.client.post(enroll_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify enrollment was created
        enrollment_exists = Enrollment.objects.filter(
            user=self.member,
            training=self.training
        ).exists()
        self.assertTrue(enrollment_exists)

    def test_enroll_full_training(self):
        # Fill up training
        member1 = User.objects.create_user(
            username='member1',
            email='member1@example.com',
            password='Pass123!'
        )
        member2 = User.objects.create_user(
            username='member2',
            email='member2@example.com',
            password='Pass123!'
        )
        Enrollment.objects.create(user=member1, training=self.training, status='confirmed')
        Enrollment.objects.create(user=member2, training=self.training, status='confirmed')

        # Try to enroll
        self.client.force_authenticate(user=self.member)
        enroll_url = reverse('sports:training-enroll', kwargs={'training_id': self.training.id})
        response = self.client.post(enroll_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_enroll_duplicate(self):
        self.client.force_authenticate(user=self.member)
        enroll_url = reverse('sports:training-enroll', kwargs={'training_id': self.training.id})

        # First enrollment
        response1 = self.client.post(enroll_url)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # Try duplicate enrollment
        response2 = self.client.post(enroll_url)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cancel_enrollment(self):
        # Create enrollment
        Enrollment.objects.create(
            user=self.member,
            training=self.training,
            status='confirmed'
        )

        # Cancel enrollment
        self.client.force_authenticate(user=self.member)
        cancel_url = reverse('sports:training-cancel', kwargs={'training_id': self.training.id})
        response = self.client.post(cancel_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify status changed
        enrollment = Enrollment.objects.get(user=self.member, training=self.training)
        self.assertEqual(enrollment.status, 'cancelled')

    def test_my_enrollments(self):
        # Create enrollment
        Enrollment.objects.create(
            user=self.member,
            training=self.training,
            status='confirmed'
        )

        self.client.force_authenticate(user=self.member)
        url = reverse('sports:my-enrollments')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)


class MembershipPlanAPITest(APITestCase):

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
        self.plan = MembershipPlan.objects.create(
            name='Bronze',
            price=100.00,
            duration_days=30,
            max_trainings_per_week=3
        )
        self.list_url = reverse('sports:plan-list')

    def test_plan_list_authenticated(self):
        self.client.force_authenticate(user=self.member)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_plan_create_admin(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            'name': 'Silver',
            'price': 150.00,
            'duration_days': 30,
            'max_trainings_per_week': 5,
            'is_active': True
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_plan_create_member_forbidden(self):
        """Test plan creation forbidden for members"""
        self.client.force_authenticate(user=self.member)
        data = {'name': 'Silver', 'price': 150.00}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MembershipAPITest(APITestCase):

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
        self.plan = MembershipPlan.objects.create(
            name='Bronze',
            price=100.00,
            duration_days=30,
            max_trainings_per_week=3
        )
        self.membership = Membership.objects.create(
            user=self.member,
            plan=self.plan,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            is_active=True
        )

    def test_my_membership(self):
        self.client.force_authenticate(user=self.member)
        url = reverse('sports:my-membership')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['plan_name'], 'Bronze')

    def test_my_membership_not_found(self):
        new_member = User.objects.create_user(
            username='newmember',
            email='new@example.com',
            password='Pass123!'
        )
        self.client.force_authenticate(user=new_member)
        url = reverse('sports:my-membership')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)