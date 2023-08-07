
from django.contrib import admin
from django.urls import path

from user_api.views import UserAPIView, ProfileAPIView, UserCreateAPIView, UserUpdateAPIView
from user_profile.views import generate_number, check_code, profile, save_invite_code

urlpatterns = [
    path('admin/', admin.site.urls),
    # API
    path('api/v1/profile/', UserAPIView.as_view()),
    path('api/v1/profile/<str:phone_number>/', ProfileAPIView.as_view(), name='profile'),
    path('api/v1/create_profile/', UserCreateAPIView.as_view(), name='create'),
    path('api/v1/update_profile/<str:phone_number>/', UserUpdateAPIView.as_view(), name='update'),
    # Страницы
    path('generate/', generate_number, name='generate_number'),
    path('check/', check_code, name='check_code'),
    path('profile/<str:phone_number>/', profile, name='profile'),
    path('save_invite_code/', save_invite_code, name='save_invite_code'),
]
