from django.contrib import admin
from .models import Sport, Training, Enrollment, MembershipPlan, Membership

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):

    list_display = ['name', 'is_active', 'trainings_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']

    fieldsets = (
        ('ძირითადი ინფორმაცია', {
            'fields': ('name', 'description', 'image')
        }),
        ('სტატუსი', {
            'fields': ('is_active',)
        }),
        ('თარიღები', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def trainings_count(self, obj):
        return obj.trainings.count()

    trainings_count.short_description = 'ვარჯიშები'


#Training admin
@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):

    list_display = [
        'title', 'sport', 'coach', 'date', 'start_time',
        'duration', 'enrolled_count_display', 'max_participants', 'is_full_display'
    ]
    list_filter = ['sport', 'coach', 'difficulty', 'date', 'is_active']
    search_fields = ['title', 'description', 'coach__first_name', 'coach__last_name']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at', 'enrolled_count', 'available_spots']
    ordering = ['-date', '-start_time']

    fieldsets = (
        ('ძირითადი ინფორმაცია', {
            'fields': ('sport', 'coach', 'title', 'description', 'difficulty')
        }),
        ('დრო და ხანგრძლივობა', {
            'fields': ('date', 'start_time', 'duration')
        }),
        ('მონაწილეები', {
            'fields': ('max_participants', 'enrolled_count', 'available_spots')
        }),
        ('სტატუსი', {
            'fields': ('is_active',)
        }),
        ('თარიღები', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def enrolled_count_display(self, obj):
        return obj.enrolled_count

    enrolled_count_display.short_description = 'ჩაწერილი'

    def is_full_display(self, obj):
        return '✓' if obj.is_full else '✗'

    is_full_display.short_description = 'სავსეა'
    is_full_display.boolean = True


# Enrollment admin
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):

    list_display = [
        'user', 'training', 'status', 'attended', 'enrolled_at'
    ]
    list_filter = ['status', 'attended', 'training__sport', 'enrolled_at']
    search_fields = [
        'user__username', 'user__first_name', 'user__last_name',
        'training__title'
    ]
    date_hierarchy = 'enrolled_at'
    readonly_fields = ['enrolled_at', 'updated_at']
    list_editable = ['status', 'attended']
    ordering = ['-enrolled_at']

    fieldsets = (
        ('ძირითადი ინფორმაცია', {
            'fields': ('user', 'training', 'status')
        }),
        ('დასწრება', {
            'fields': ('attended', 'notes')
        }),
        ('თარიღები', {
            'fields': ('enrolled_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


#Membership plan admin
@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    """საწევროს პაკეტების მართვა"""

    list_display = [
        'name', 'price', 'duration_days', 'max_trainings_per_week',
        'is_active', 'members_count'
    ]
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['price']

    fieldsets = (
        ('ძირითადი ინფორმაცია', {
            'fields': ('name', 'description')
        }),
        ('პირობები', {
            'fields': ('price', 'duration_days', 'max_trainings_per_week')
        }),
        ('სტატუსი', {
            'fields': ('is_active',)
        }),
        ('თარიღები', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def members_count(self, obj):
        """რამდენი წევრი იყენებს"""
        return obj.memberships.filter(is_active=True).count()

    members_count.short_description = 'აქტიური წევრები'


# ======= MEMBERSHIP ADMIN =======
@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    """საწევროების მართვა"""

    list_display = [
        'user', 'plan', 'start_date', 'end_date',
        'is_active', 'is_expired_display', 'auto_renew'
    ]
    list_filter = ['plan', 'is_active', 'auto_renew', 'start_date']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at', 'updated_at', 'is_expired']
    list_editable = ['is_active', 'auto_renew']
    ordering = ['-start_date']

    fieldsets = (
        ('ძირითადი ინფორმაცია', {
            'fields': ('user', 'plan')
        }),
        ('პერიოდი', {
            'fields': ('start_date', 'end_date', 'is_expired')
        }),
        ('პარამეტრები', {
            'fields': ('is_active', 'auto_renew')
        }),
        ('თარიღები', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    #თუ არის ვადაგასული
    def is_expired_display(self, obj):
        return '✓' if obj.is_expired else '✗'

    is_expired_display.short_description = 'ვადაგასულია'
    is_expired_display.boolean = True