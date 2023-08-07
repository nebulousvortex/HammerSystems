import re

from .generators import generate_code, generate_referral
from .models import Users
from django.shortcuts import render, redirect
from django.contrib import messages



def generate_number(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']

        # Проверка формата номера
        if not re.match(r'^\d{11}$', phone_number):
            messages.error(request, 'Неправильный формат номера телефона.')
            return redirect('generate_number')

        try:
            # Проверка, существует ли номер в базе данных
            existing_number = Users.objects.get(phone_number=phone_number)
            code = generate_code()
            # Сохранение кода и номера
            request.session['generated_code'] = code
            request.session['existing_number'] = phone_number
            existing_number.save()
            messages.success(request, f'Ваш сгенерированный код: {code}')

        except Users.DoesNotExist:
            # Если номера нет в базе данных, добавляем его
            Users.objects.create(phone_number=phone_number, referral_code=generate_referral())
            code = generate_code()
            # Сохранение номера и кода
            request.session['generated_code'] = code
            request.session['existing_number'] = phone_number
            messages.success(request, f'Номер добавлен в базу данных. Ваш сгенерированный код: {code}')

        return redirect('check_code')

    return render(request, 'user_profile/generate_number.html')


def check_code(request):
    generated_code = request.session.get('generated_code')
    phone_number = request.session.get('existing_number')
    if request.method == 'POST':
        entered_code = request.POST['code']
        if int(entered_code) == int(generated_code):
            return redirect('profile', phone_number=phone_number)
        else:
            messages.error(request, 'Введенный код неверный!')

    return render(request, 'user_profile/check_code.html', {'generated_code': generated_code})

def profile(request, phone_number):
    user = Users.objects.get(phone_number=phone_number)
    return render(request, 'user_profile/profile.html', {'user': user})

def save_invite_code(request):
    if request.method == 'POST':
        invite_code = request.POST['invite_code']
        user = Users.objects.get(phone_number=request.session.get('existing_number'))

        if invite_code == user.referral_code:
            messages.error(request, 'Вы не можете использовать свой собственный реферальный код.')
        elif Users.objects.filter(referral_code=invite_code).exists():
            user.invite_code = invite_code
            user.save()
            messages.success(request, 'Код приглашения сохранен успешно.')
        else:
            messages.error(request, 'Введенный реферальный код не существует.')

        return redirect('profile', phone_number=user.phone_number)