from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from .models import User, PasswordResetToken
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    UserProfileSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    PasswordChangeSerializer
)
from .permissions import IsAdmin, IsOwnerOrAdmin


#momxmareblis registracia
class UserRegistrationView(APIView):
    permission_classes = []

    def post(self, request):
        #POST /api/auth/register/
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            #JWT Token - ების გენერაცია
            refresh = RefreshToken.for_user(user)

            return Response({
                'message': 'რეგისტრაცია წარმატებით დასრულდა',
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#avtorizacia
class UserLoginView(APIView):

    permission_classes = []

    def post(self, request):
        serializer = UserLoginSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            return Response({
                'message': 'ავტორიზაცია წარმატებით დასრულდა',
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            return Response({
                'message': 'წარმატებით გახვედით სისტემიდან'
            }, status=status.HTTP_200_OK)
        except Exception:
            return Response({
                'error': 'რაღაც არასწორად მოხდა'
            }, status=status.HTTP_400_BAD_REQUEST)



class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    filterset_fields = ['role', 'is_active_member']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering_fields = ['date_joined', 'username']


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrAdmin]



class CurrentUserView(APIView):
    """GET/PUT /api/users/me/ - ჩემი პროფილი"""

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'პროფილი განახლდა',
                'user': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PasswordResetRequestView(APIView):
    """POST /api/auth/password-reset/ - პაროლის აღდგენა"""
    permission_classes = []

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)


            reset_token = PasswordResetToken.create_token(user)


            reset_link = f"http://localhost:8000/reset-password/{reset_token.token}"

            send_mail(
                subject='პაროლის აღდგენა - MMA Club',
                message=f'გამარჯობა {user.first_name}!\n\n'
                        f'პაროლის აღდგენის ლინკი:\n{reset_link}\n\n'
                        f'ეს ლინკი ვალიდურია 1 საათის განმავლობაში.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            return Response({
                'message': 'პაროლის აღდგენის ინსტრუქცია გაიგზავნა თქვენს ელ-ფოსტაზე'
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PasswordResetConfirmView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)

        if serializer.is_valid():
            reset_token = serializer.validated_data['reset_token']
            new_password = serializer.validated_data['password']


            user = reset_token.user
            user.set_password(new_password)
            user.save()


            reset_token.mark_as_used()

            return Response({
                'message': 'პაროლი წარმატებით შეიცვალა'
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordChangeView(APIView):

    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'პაროლი წარმატებით შეიცვალა'
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)