from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import UsersSerializer, UserSerializer, UserCreatorSerializer, UsersUpdateSerializer
from user_profile.models import Users


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersUpdateSerializer
    lookup_field = 'phone_number'

    def update(self, request, *args, **kwargs):
        # Получение данные из запроса
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        phone_number = self.kwargs.get('phone_number')

        invite_code = request.data.get('invite_code')
        user = Users.objects.get(phone_number=phone_number)
        # Проверяем invite_code
        if invite_code:
            if user.invite_code:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if invite_code == user.referral_code:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            elif Users.objects.filter(referral_code=invite_code).exists():
                user.invite_code = invite_code
                user.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)
        return Response(serializer.data)

class UserAPIView(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

class UserCreateAPIView(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserCreatorSerializer

class ProfileAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = Users.objects.all()

    def get_object(self):
        phone_number = self.kwargs['phone_number']
        user = Users.objects.get(phone_number=phone_number)

        return user
