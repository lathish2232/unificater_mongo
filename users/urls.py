from django.urls import path

from users.views import register_user, login_user, logout, forgot_unify_password, reset_password, \
    get_user_profile, change_password

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('logout', logout),
    path('password/forgot', forgot_unify_password),
    path('password/reset', reset_password),
    path('password/change', change_password),
    path('profile', get_user_profile),
]
