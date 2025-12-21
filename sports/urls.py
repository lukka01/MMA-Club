from django.urls import path
from .views import (
    #Sport Views
    SportListCreateView,
    SportDetailView,

    #Training Views
    TrainingListCreateView,
    TrainingDetailView,
    UpcomingTrainingsView,
    MyTrainingsView,

    #Enrollment Views
    TrainingEnrollView,
    TrainingCancelEnrollmentView,
    MyEnrollmentsView,
    TrainingEnrollmentsView,

    #Membership Views
    MembershipPlanListCreateView,
    MembershipPlanDetailView,
    MembershipListCreateView,
    MyMembershipView,
)
app_name = 'sports'

urlpatterns = [
    #Sports
    path('sports/', SportListCreateView.as_view(), name='sport-list'),
    path('sports/<int:pk>/', SportDetailView.as_view(), name='sport-detail'),

    #Trainigs
    path('trainings/', TrainingListCreateView.as_view(), name='training-list'),
    path('trainings/upcoming/', UpcomingTrainingsView.as_view(), name='training-upcoming'),
    path('trainings/my-trainings/', MyTrainingsView.as_view(), name='my-trainings'),
    path('trainings/<int:pk>/', TrainingDetailView.as_view(), name='training-detail'),
    path('trainings/<int:training_id>/enroll/', TrainingEnrollView.as_view(), name='training-enroll'),
    path('trainings/<int:training_id>/cancel-enrollment/', TrainingCancelEnrollmentView.as_view(),
         name='training-cancel'),
    path('trainings/<int:training_id>/enrollments/', TrainingEnrollmentsView.as_view(), name='training-enrollments'),

    #Enrollments
    path('enrollments/my-enrollments/', MyEnrollmentsView.as_view(), name='my-enrollments'),

    #Membership plans
    path('membership-plans/', MembershipPlanListCreateView.as_view(), name='plan-list'),
    path('membership-plans/<int:pk>/', MembershipPlanDetailView.as_view(), name='plan-detail'),

    #Membership
    path('memberships/', MembershipListCreateView.as_view(), name='membership-list'),
    path('memberships/my-membership/', MyMembershipView.as_view(), name='my-membership'),
]