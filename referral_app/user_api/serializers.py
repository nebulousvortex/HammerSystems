from rest_framework import serializers

from user_profile.generators import generate_referral
from user_profile.models import Users

# Сериализатор вывода конкретного пользователя с его реферальными клиентами
class UserSerializer(serializers.ModelSerializer):
    referral_numbers = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ['phone_number', 'referral_code', 'invite_code', 'referral_numbers']

    def get_referral_numbers(self, obj):
        referral_codes = Users.objects.filter(invite_code=obj.referral_code).values_list('phone_number', flat=True)
        return list(referral_codes)

# Сериализатор вывода всех пользователей
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['phone_number', 'referral_code', 'invite_code']


# Сериализатор обновления одного пользователя
class UsersUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['invite_code']


# Сериализатор создания одного пользователя
class UserCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['phone_number']

    def create(self, validated_data):
        # Генерация реферального кода
        referral_code = generate_referral()
        validated_data['referral_code'] = referral_code
        user = super().create(validated_data)
        return user
