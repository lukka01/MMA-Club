from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Sport, Training, Enrollment, MembershipPlan, Membership
from .serializers import (
    SportSerializer,
    TrainingSerializer,
    TrainingListSerializer,
    EnrollmentSerializer,
    MyEnrollmentSerializer,
    MembershipPlanSerializer,
    MembershipSerializer
)
from users.permissions import IsAdmin, IsAdminOrCoach


class SportListCreateView(generics.ListCreateAPIView):
    """
    GET /api/sports/ - ყველა სპორტი
    POST /api/sports/ - ახალი სპორტის დამატბა
    """
    queryset = Sport.objects.filter(is_active=True)
    serializer_class = SportSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [IsAuthenticated()]


class SportDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/sports/{id}/ - კონკრეტული სპორტი
    PUT /api/sports/{id}/ - განახლება (Admin)
    DELETE /api/sports/{id}/ - წაშლა (admin)
    """
    queryset = Sport.objects.all()
    serializer_class = SportSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAdmin()]


class TrainingListCreateView(generics.ListCreateAPIView):
    """
    GET /api/trainings/ - ყველა ვარჯიში
    POST /api/trainings/ - ახალი ვარჯიშის შექმნა (Admin/Coach)
    """
    queryset = Training.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sport', 'coach', 'difficulty', 'date']
    search_fields = ['title', 'description']
    ordering_fields = ['date', 'start_time', 'created_at']
    ordering = ['date', 'start_time']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TrainingListSerializer
        return TrainingSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminOrCoach()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(coach=self.request.user)


class TrainingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/trainings/{id}/ -კონკრტული ვარჯიში
    PUT /api/trainings/{id}/ - განახლება (Admin/coach)
    DELETE /api/trainings/{id}/ -წაშლა (Admin/Coach)
    """
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAdminOrCoach()]


class UpcomingTrainingsView(generics.ListAPIView):
    """GET /api/trainings/upcoming/ - მომავალი ვარჯიშები"""
    serializer_class = TrainingListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Training.objects.filter(
            is_active=True,
            date__gte=timezone.now().date()
        ).order_by('date', 'start_time')


class MyTrainingsView(generics.ListAPIView):
    """GET /api/trainings/my-trainings/ - ჩემი ვარჯიშები (როცა coach ვარ)"""
    serializer_class = TrainingListSerializer
    permission_classes = [IsAdminOrCoach]

    def get_queryset(self):
        return Training.objects.filter(
            coach=self.request.user,
            is_active=True
        ).order_by('-date', '-start_time')


#Enrollment views

class TrainingEnrollView(APIView):
    """POST /api/trainings/training_id/enroll/ -ვარჯიშზე ჩაწერა"""
    permission_classes = [IsAuthenticated]

    def post(self, request, training_id):
        try:
            training = Training.objects.get(id=training_id, is_active=True)
        except Training.DoesNotExist:
            return Response(
                {'error': 'ვარჯიში არ მოიძებნა'},
                status=status.HTTP_404_NOT_FOUND
            )

        # სავსე არის თუ არა
        if training.is_full:
            return Response(
                {'error': 'ვარჯიში სავსეა'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # უკვე ჩაწერილია თუ არა
        if Enrollment.objects.filter(
                user=request.user,
                training=training,
                status__in=['confirmed', 'pending']
        ).exists():
            return Response(
                {'error': 'თქვენ უკვე ჩაწერილი ხართ'},
                status=status.HTTP_400_BAD_REQUEST
            )

        #ჩაწერის შექმნა
        enrollment = Enrollment.objects.create(
            user=request.user,
            training=training,
            status='confirmed'
        )

        serializer = EnrollmentSerializer(enrollment)
        return Response({
            'message': 'წარმატებით ჩაიწერეთ ვარჯიშზე',
            'enrollment': serializer.data
        }, status=status.HTTP_201_CREATED)


class TrainingCancelEnrollmentView(APIView):
    """POST /api/trainings/{training_id}/cancel-enrollment/ - ჩაწერის გაუქმება"""
    permission_classes = [IsAuthenticated]

    def post(self, request, training_id):
        try:
            enrollment = Enrollment.objects.get(
                user=request.user,
                training_id=training_id,
                status__in=['confirmed', 'pending']
            )
        except Enrollment.DoesNotExist:
            return Response(
                {'error': 'ჩაწერა არ მოიძებნა'},
                status=status.HTTP_404_NOT_FOUND
            )

        enrollment.status = 'cancelled'
        enrollment.save()

        return Response({
            'message': 'ჩაწერა გაუქმდა'
        }, status=status.HTTP_200_OK)


class MyEnrollmentsView(generics.ListAPIView):
    """GET /api/enrollments/my-enrollments/ - ჩემი ჩაწერები"""
    serializer_class = MyEnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(
            user=self.request.user
        ).select_related('training', 'training__sport', 'training__coach')


class TrainingEnrollmentsView(generics.ListAPIView):
    """GET /api/trainings/{training_id}/enrollments/ - ვარჯიშის ჩაწერები (Coach/Admin)"""
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAdminOrCoach]

    def get_queryset(self):
        training_id = self.kwargs.get('training_id')
        return Enrollment.objects.filter(
            training_id=training_id
        ).select_related('user', 'training')


#Membership Views

class MembershipPlanListCreateView(generics.ListCreateAPIView):
    """
    GET /api/membership-plans/ - ყველა პაკეტი
    POST /api/membership-plans/ -ახალი პაკეტის დამატება (Admin)
    """
    queryset = MembershipPlan.objects.filter(is_active=True)
    serializer_class = MembershipPlanSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [IsAuthenticated()]


class MembershipPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/membership-plans/{id}/ - კონკრეტული პაკეტი
    PUT /api/membership-plans/{id}/ - განახლება (Admin)
    DELETE /api/membership-plans/{id}/ - წაშლა (Admin)
    """
    queryset = MembershipPlan.objects.all()
    serializer_class = MembershipPlanSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAdmin()]


class MembershipListCreateView(generics.ListCreateAPIView):
    """
    GET /api/memberships/ - ყველა საწევრო (Admin)
    POST /api/memberships/ - ახალი საწევროს შექმნა (Admin)
    """
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user', 'plan', 'is_active']
    ordering_fields = ['start_date', 'end_date']


class MyMembershipView(APIView):
    """GET /api/memberships/my-membership/ - ჩემი საწევრო"""
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            membership = Membership.objects.filter(
                user=request.user,
                is_active=True
            ).select_related('plan').latest('start_date')

            serializer = MembershipSerializer(membership)
            return Response(serializer.data)
        except Membership.DoesNotExist:
            return Response(
                {'message': 'თქვენ არ გაქვთ აქტიური საწევრო'},
                status=status.HTTP_404_NOT_FOUND
            )
