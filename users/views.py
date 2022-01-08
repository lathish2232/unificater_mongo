from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

# Create your views here.
from users.user_impl import create_user, user_login, logout_user, forgot_password, reset_pswd, \
    user_profile, change_pswd


@csrf_exempt
@api_view(['POST'])
def register_user(request):
    return create_user(request)


@csrf_exempt
@api_view(['POST'])
def login_user(request):
    return user_login(request)


@csrf_exempt
@api_view(['DELETE'])
def logout(request):
    return logout_user(request)


@csrf_exempt
@api_view(['POST'])
def forgot_unify_password(request):
    return forgot_password(request)


@csrf_exempt
@api_view(['POST'])
def reset_password(request):
    return reset_pswd(request)


@csrf_exempt
@api_view(['POST'])
def change_password(request):
    return change_pswd(request)


@csrf_exempt
@api_view(['GET'])
def get_user_profile(request):
    return user_profile(request)
