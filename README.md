# HammerSystems
Тестовое задание от Hammer Systems

- GET /api/v1/profile: возвращает список всех profile_user и их атрибуты.
- GET /api/v1/profile/{phone_number}: Возвращает все атрибуты конкретного пользователя и список тех, кто использует его referral_code
- GET /api/v1/create_profile: созвращает список уже имеющихся phone_number
- POST /api/v1/create_profile: создает новый profile_user
- PUT /api/v1/update_profile/{phone_number}: обновляет invite_code на чужой существующий referral_code
