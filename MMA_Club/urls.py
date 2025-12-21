from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="MMA Club API",
        default_version='v1',
        description="""
         MMA სპორტული კლუბის მართვის სისტემა

        ## ფუნქციონალი:
        - User Authentication (JWT)
        - სპორტები და ვარჯიშები
        - ვარჯიშებზე ჩაწერა
        - აწევროს მართვა
        - Role-based Access Control (Admin, Coach, Member)
        - Password Reset with Email

        ## როლები:
        - **Admin** - სრული წვდომა
        - **Coach** - ვარჯიშების შექმნა/მართვა
        - **Member** - ვარჯიშებზე ჩაწერა

        ## Authentication:
        1. Register: POST /api/auth/register/
        2. Login: POST /api/auth/login/ (მიიღებ access და refresh tokens)
        3. დაამატე Header: `Authorization: Bearer <access_token>`
        """,
        contact=openapi.Contact(email="contact@mmaclub.ge"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    #Admin panel
    path('admin/', admin.site.urls),

    #Api endpoints
    path('api/auth/', include('users.urls')),  # Authentication & Users
    path('api/', include('sports.urls')),  # Sports, Trainings, Memberships

    #Api documentation
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
    path('api/docs/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]

#media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#Admin panel customization
admin.site.site_header = "MMA Club - ადმინისტრაციული პანელი"
admin.site.site_title = "MMA Club Admin"
admin.site.index_title = "მართვის პანელი"