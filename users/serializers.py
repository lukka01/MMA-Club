
#User Serializers - მონაცემების ვალიდაციები და JSON გარდაქმნა

from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, PasswordResetToken


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone', 'birth_date', 'address'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "პაროლები არ ემთხვევა."})
        return attrs

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("ეს ელ-ფოსტა უკვე გამოყენებულია.")
        return value

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            birth_date=validated_data.get('birth_date'),
            address=validated_data.get('address', ''),
            role='member'
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    #avtorizaciisTvis
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )
            if not user:
                raise serializers.ValidationError(
                    'მომხმარებლის სახელი ან პაროლი არასწორია.',
                    code='authorization'
                )
        else:
            raise serializers.ValidationError(
                'გთხოვთ შეიყვანოთ მომხმარებლის სახელი და პაროლი.',
                code='authorization'
            )

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    #Useristvis
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'role', 'phone', 'birth_date', 'address',
            'profile_image', 'membership_start', 'is_active_member',
            'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'username', 'date_joined', 'last_login', 'membership_start']

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if 'role' in validated_data and not (request and request.user.is_admin):
            validated_data.pop('role')
        return super().update(instance, validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    #საკუთარი პროფილის
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'role', 'phone', 'birth_date', 'address',
            'profile_image', 'membership_start', 'is_active_member'
        ]
        read_only_fields = ['id', 'username', 'role', 'membership_start']


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("მომხმარებელი ამ ელ-ფოსტით არ არსებობს.")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "პაროლები არ ემთხვევა."})

        try:
            reset_token = PasswordResetToken.objects.get(token=attrs['token'])
            if not reset_token.is_valid():
                raise serializers.ValidationError({"token": "ტოკენი არავალიდურია ან ვადაგასულია."})
            attrs['reset_token'] = reset_token
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError({"token": "ტოკენი არ არსებობს."})

        return attrs


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    new_password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("ძველი პაროლი არასწორია.")
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "პაროლები არ ემთხვევა."})
        return attrs

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user