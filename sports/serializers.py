from rest_framework import serializers
from django.utils import timezone
from .models import Sport, Training, Enrollment, MembershipPlan, Membership
from users.serializers import UserSerializer



class SportSerializer(serializers.ModelSerializer):
    trainings_count = serializers.SerializerMethodField()

    class Meta:
        model = Sport
        fields = ['id', 'name', 'description', 'image', 'is_active', 'trainings_count', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_trainings_count(self, obj):
        return obj.trainings.filter(is_active=True).count()

class TrainingSerializer(serializers.ModelSerializer):
    sport_name = serializers.CharField(source='sport.name', read_only=True)
    coach_name = serializers.CharField(source='coach.get_full_name', read_only=True)
    enrolled_count = serializers.IntegerField(read_only=True)
    is_full = serializers.BooleanField(read_only=True)
    available_spots = serializers.IntegerField(read_only=True)
    is_enrolled = serializers.SerializerMethodField()

    class Meta:
        model = Training
        fields = [
            'id', 'sport', 'sport_name', 'coach', 'coach_name',
            'title', 'description', 'difficulty', 'date', 'start_time',
            'duration', 'max_participants', 'enrolled_count', 'is_full',
            'available_spots', 'is_enrolled', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'enrolled_count', 'is_full', 'available_spots']

    def get_is_enrolled(self, obj):
        #მიმდინარე იუზერი არის თუ არა ჩაწეილი
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Enrollment.objects.filter(
                user=request.user,
                training=obj,
                status='confirmed'
            ).exists()
        return False

    def validate_coach(self, value):
        #ვამოწმებთ არის თუ არა მწვრთნელი
        if value.role not in ['admin', 'coach']:
            raise serializers.ValidationError("მწვრთნელი უნდა იყოს admin ან coach როლით.")
        return value

    def validate(self, attrs):
        date = attrs.get('date')
        start_time = attrs.get('start_time')
        coach = attrs.get('coach')

        if not self.instance:  # ახალი ვარჯიშის შექმნა
            # თარიღი არ უნდა იყოს წარსულში
            if date < timezone.now().date():
                raise serializers.ValidationError({"date": "თარიღი არ შეიძლება იყოს წარსულში."})

            #მწვრთნელს არ უნდა ჰქონდეს ვარჯიში იმავე დროს
            if Training.objects.filter(coach=coach, date=date, start_time=start_time).exists():
                raise serializers.ValidationError("მწვრთნელს უკვე აქვს ვარჯიში ამ დროს.")

        return attrs


class TrainingListSerializer(serializers.ModelSerializer):
    sport_name = serializers.CharField(source='sport.name', read_only=True)
    coach_name = serializers.CharField(source='coach.get_full_name', read_only=True)
    enrolled_count = serializers.IntegerField(read_only=True)
    available_spots = serializers.IntegerField(read_only=True)

    class Meta:
        model = Training
        fields = [
            'id', 'sport_name', 'coach_name', 'title',
            'difficulty', 'date', 'start_time', 'duration',
            'enrolled_count', 'available_spots'
        ]

class EnrollmentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    training_title = serializers.CharField(source='training.title', read_only=True)
    training_date = serializers.DateField(source='training.date', read_only=True)
    training_time = serializers.TimeField(source='training.start_time', read_only=True)

    class Meta:
        model = Enrollment
        fields = [
            'id', 'user', 'user_name', 'training', 'training_title',
            'training_date', 'training_time', 'status', 'attended',
            'notes', 'enrolled_at'
        ]
        read_only_fields = ['id', 'enrolled_at', 'user']

    def validate(self, attrs):
        training = attrs.get('training')
        user = self.context['request'].user

        if not self.instance:  # ახალი ჩაწერა
            if training.is_full:
                raise serializers.ValidationError("ვარჯიში სავსეა. ადგილები აღარ არის.")

            if Enrollment.objects.filter(
                    user = user,
                    training =training,
                    status__in = ['confirmed', 'pending']
            ).exists():
                raise serializers.ValidationError("თქვენ უკვე ჩაწერილი ხართ ამ ვარჯიშზე.")

        return attrs


class MyEnrollmentSerializer(serializers.ModelSerializer):
    training = TrainingListSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'training', 'status', 'attended', 'enrolled_at']


class MembershipPlanSerializer(serializers.ModelSerializer):
    members_count = serializers.SerializerMethodField()

    class Meta:
        model = MembershipPlan
        fields = [
            'id', 'name', 'description', 'price', 'duration_days',
            'max_trainings_per_week', 'is_active', 'members_count'
        ]
        read_only_fields = ['id']

    def get_members_count(self, obj):
        #aqtiuri wevrebis raodenoba
        return obj.memberships.filter(is_active=True).count()


#membership serializer
class MembershipSerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    plan_name = serializers.CharField(source='plan.name', read_only=True)
    plan_details = MembershipPlanSerializer(source='plan', read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    days_remaining = serializers.SerializerMethodField()

    class Meta:
        model = Membership
        fields = [
            'id', 'user', 'user_name', 'plan', 'plan_name', 'plan_details',
            'start_date', 'end_date', 'is_active', 'is_expired',
            'days_remaining', 'auto_renew', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'user']

    def get_days_remaining(self, obj):
        if obj.is_expired:
            return 0
        delta = obj.end_date - timezone.now().date()
        return delta.days

    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')

        if start_date and end_date:
            if end_date <= start_date:
                raise serializers.ValidationError({
                    "end_date": "დასრულების თარიღი უნდა იყოს დაწყების თარიღზე გვიან!"
                })
        return attrs