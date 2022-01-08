import datetime
import time
import traceback
from hashlib import blake2b

import dateutil.parser
import pytz
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response

from service.util.mailer import send_reset_mail
from service.util.unify_logger import unify_printer, UNIFY_ERROR, UNIFY_DEBUG
from service.util.unify_response import internal_server_response, success_response, \
    create_response, unauthorized, no_content_response, forbidden_response, validation_error_response, \
    success_response_v1
from unificater.settings import RESET_KEY_EXP, TOKEN_HEADER
from users.UserDetails import UserDetails
from users.user_db_untils import get_user_mongod_connection
from users.web_token import get_token_user, delete_token, store_token, generate_token


def create_user(request):
    try:
        user = request.data
        unify_printer(message=f"user: {user}")
        mongod = get_user_mongod_connection()
        result = mongod['users'].insert_one(user)
        response = create_response(message=f'User \'{user["name"]}\' Created Successfully!')
        json_response = JsonResponse(response, status=status.HTTP_200_OK)

    except Exception as ex:
        unify_printer(level=UNIFY_ERROR, message='Exception occurred while create user', error=ex,
                      traceback=traceback.format_exc())
        response = internal_server_response('Error while create user', traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response


def user_login(request):
    try:
        credentials = request.data
        mongod = get_user_mongod_connection()
        user = mongod['users'].find_one({'name': credentials["name"].upper()})
        if user:
            if not user['isLocked']:
                if user["password"] == credentials["password"]:
                    unify_printer(message=f"Login Success for the USER: {credentials['name']}")
                    token = generate_token(user["name"])
                    if token:
                        response = success_response(data={"authToken": token})
                        store_token(user["name"], token)
                        json_response = Response()
                        json_response.data = response
                        json_response.status_code = status.HTTP_200_OK
                    else:
                        response = internal_server_response("Technical issue in login, Try after sometime.", None)
                        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                else:
                    response = unauthorized("Invalid Credentials")
                    json_response = JsonResponse(response, status=status.HTTP_401_UNAUTHORIZED)
            else:
                unify_printer(level=UNIFY_DEBUG, message="User LOCKED...")
                response = unauthorized("User Locked, Contact Admin for unlock")
                json_response = JsonResponse(response, status=status.HTTP_401_UNAUTHORIZED)
        else:
            unify_printer(message="User not found...")
            response = unauthorized("Invalid Credentials")
            json_response = JsonResponse(response, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as ex:
        unify_printer(level=UNIFY_ERROR, message='Exception occurred while login', error=ex,
                      traceback=traceback.format_exc())
        response = internal_server_response('Error while login', traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response


def logout_user(request):
    token = request.headers.get(TOKEN_HEADER)
    if token:
        json_response = Response()
        # request.session[token] = '0'
        # cache.delete(token)
        # if request.session.test_cookie_worked():
        #     request.session.delete_test_cookie()
        delete_token(token)
        response = success_response_v1(message="Logout Successfully!")
        json_response.data = response
        json_response.status_code = status.HTTP_200_OK
    else:
        unify_printer(level=UNIFY_ERROR, message='Error while logout...', error=None,
                      traceback=None)
        response = internal_server_response("Error while logout...", None)
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response


def forgot_password(request):
    try:
        user_name = request.data.get('name')
        mongod = get_user_mongod_connection()
        query = {'name': user_name.upper()}
        user = mongod['users'].find_one(query)
        if user:
            mail_id = user.get('emailId')
            to = mail_id if mail_id else 'admin@unificater.com'
            now = datetime.datetime.now()
            resetKeyExp = now + datetime.timedelta(minutes=RESET_KEY_EXP)
            reset_key = blake2b(f'{user_name}_{now}'.encode("utf-8")).hexdigest()
            update_val = {
                "$set": {"resetKey": reset_key, "resetKeyExp": resetKeyExp,
                         "isLocked": True, "modifiedBy": user_name, "modifiedOn": datetime.datetime.now()}}
            update_result = mongod['users'].update_one(query, update_val)
            send_reset_mail(to, reset_key)
            response = success_response_v1(message=f"Reset link sent to your mail {to}")
        else:
            response = no_content_response(message=f"Usr not found")
        json_response = JsonResponse(response, status=status.HTTP_200_OK)
    except Exception as ex:
        unify_printer(level=UNIFY_ERROR, message='Exception occurred while forgot password', error=ex,
                      traceback=traceback.format_exc())
        response = internal_server_response('Error in forgot password', traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response


def reset_pswd(request):
    try:
        user_name = request.data.get('name')
        reset_key = request.data.get('resetKey')
        mongod = get_user_mongod_connection()
        query = {'name': user_name.upper(), 'resetKey': reset_key}
        user = mongod['users'].find_one(query)
        if user:
            if user.get('isLocked'):
                reset_key_exp = user.get('resetKeyExp')
                now = datetime.datetime.now()
                if now <= reset_key_exp:
                    password = request.data.get('password')
                    update_val = {
                        "$set": {"password": password, "isLocked": False, "modifiedBy": user_name,
                                 "modifiedOn": datetime.datetime.now()}}
                    update_result = mongod['users'].update_one(query, update_val)
                    response = success_response_v1(message=f"Password reset successfully")
                    json_response = JsonResponse(response, status=status.HTTP_200_OK)
                else:
                    response = forbidden_response("Link Expired")
                    json_response = JsonResponse(response, status=status.HTTP_403_FORBIDDEN)
            else:
                response = forbidden_response("Link already closed")
                json_response = JsonResponse(response, status=status.HTTP_403_FORBIDDEN)
        else:
            unify_printer(message="User not found...")
            response = no_content_response("User/Link Not Valid")
            json_response = JsonResponse(response, status=status.HTTP_200_OK)
    except Exception as ex:
        unify_printer(level=UNIFY_ERROR, message='Exception occurred while reset password', error=ex,
                      traceback=traceback.format_exc())
        response = internal_server_response('Error while reset password.', traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response


def change_pswd(request):
    try:
        user_name = request.data.get('name')
        mongod = get_user_mongod_connection()
        query = {'name': user_name.upper()}
        user = mongod['users'].find_one(query)
        if user:
            password = request.data.get('password')
            update_val = {
                "$set": {"password": password, "isLocked": False, "modifiedBy": user_name,
                         "modifiedOn": datetime.datetime.now()}}
            update_result = mongod['users'].update_one(query, update_val)
            response = success_response_v1(message=f"Password changed successfully")
            json_response = JsonResponse(response, status=status.HTTP_200_OK)
        else:
            unify_printer(message="User not found...")
            response = no_content_response("User Not Valid")
            json_response = JsonResponse(response, status=status.HTTP_200_OK)
    except Exception as ex:
        unify_printer(level=UNIFY_ERROR, message='Exception occurred while change password', error=ex,
                      traceback=traceback.format_exc())
        response = internal_server_response("Error while change password.", traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response


def user_profile(request):
    try:
        token = request.headers.get(TOKEN_HEADER)
        user_name = get_token_user(token)
        if user_name:
            mongod = get_user_mongod_connection()
            user = mongod['users'].find_one({'name': user_name.upper()},
                                            {"_id": 0, "password": 0, "isLocked": 0, "resetKey": 0, "resetKeyExp": 0})
            if user:
                created_date = user.get('createdOn')
                if created_date:
                    utctime = dateutil.parser.parse(str(created_date))
                    est_time = utctime.astimezone(pytz.timezone("Canada/Eastern")).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                    user['createdOn'] = est_time
                update_date = user.get('modifiedOn')
                if update_date:
                    utctime = dateutil.parser.parse(str(update_date))
                    est_time = utctime.astimezone(pytz.timezone("Canada/Eastern")).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                    user['modifiedOn'] = est_time
                response = success_response(data=user)
            else:
                response = validation_error_response("User Not found in the token.")
        else:
            response = validation_error_response("User Not found in the token.")
        json_response = JsonResponse(response, status=status.HTTP_200_OK)
    except Exception as ex:
        unify_printer(level=UNIFY_ERROR, message='Exception occurred while get user profile', error=ex,
                      traceback=traceback.format_exc())
        response = internal_server_response('Error while get user', traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response


def get_userid_by_name(user_name):
    try:
        mongod = get_user_mongod_connection()
        user = mongod['users'].find_one({'name': user_name.upper()},
                                        {"_id": 0, "name": 0, "password": 0, "isLocked": 0, "resetKey": 0,
                                         "resetKeyExp": 0, "modifiedBy": 0, "modifiedOn": 0, "createdBy": 0,
                                         "createdOn": 0})
        UserDetails.LOGGED_IN_USER_NAME = user_name
        UserDetails.LOGGED_IN_USER_ID = user['userId']
    except Exception as ex:
        unify_printer(level=UNIFY_ERROR, message='Exception occurred while get user id by name', error=ex,
                      traceback=traceback.format_exc())
