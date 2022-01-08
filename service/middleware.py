import json
import time
import traceback
from uuid import uuid4

import jwt
from django.http import JsonResponse
from rest_framework import status

from service.util.unify_logger import unify_printer, UNIFY_ERROR, unify_audit_printer, insert_unify_log
from service.util.unify_response import unauthorized, internal_server_response, service_unavailable
from unificater.settings import SECRET_KEY, ALGORITHM, TOKEN_HEADER, AUTH_EXCLUDE
from users.UserDetails import UserDetails
from users.web_token import get_token, delete_token, generate_token, store_token


class TokenValidation(object):

    def __init__(self, get_response):
        UserDetails.clear_user_details(UserDetails)
        unify_printer(message="Initializing TokenValidation...")
        self.get_response = get_response
        self.error = None
        insert_unify_log()
        UserDetails.clear_user_details(UserDetails)

    def __call__(self, request):
        response = self.process_request(request)
        return response

    def process_request(self, request):
        start = time.time()
        try:
            UserDetails.clear_user_details(UserDetails)
            path = request.path
            UserDetails.REQUEST_API = path
            UserDetails.CORRELATION_ID = str(uuid4())
            if path not in AUTH_EXCLUDE:
                token = request.headers.get(TOKEN_HEADER)
                if token:
                    unify_printer(message='Token received, verifying Token...')
                    token_status = get_token(token)
                    if token_status == 'TRUE':
                        is_valid = self.verify_token(token)
                        if is_valid:
                            unify_printer(
                                message=f"Token verified for the User {UserDetails.LOGGED_IN_USER_NAME}, Processing "
                                        f"Request")
                            response = self.get_response(request)
                        else:
                            unify_printer(level=UNIFY_ERROR, message=f"error: {self.error}")
                            response = unauthorized(self.error)
                            response = JsonResponse(response, status=status.HTTP_401_UNAUTHORIZED)
                    elif token_status == 'FALSE':
                        unify_printer(message='Token NOT valid')
                        response = unauthorized("Session not alive or Logged in from different platform")
                        response = JsonResponse(response, status=status.HTTP_401_UNAUTHORIZED)
                    else:
                        unify_printer(message=token_status)
                        response = service_unavailable(token_status)
                        response = JsonResponse(response, status=status.HTTP_503_SERVICE_UNAVAILABLE)
                else:
                    unify_printer(message="Token NOT Received")
                    response = unauthorized("Token not available")
                    response = JsonResponse(response, status=status.HTTP_401_UNAUTHORIZED)
            else:
                response = self.get_response(request)
        except jwt.ExpiredSignatureError as ex:
            delete_token(token)
            token = generate_token(UserDetails.LOGGED_IN_USER_NAME)
            store_token(UserDetails.LOGGED_IN_USER_NAME, token)
            self.error = "New token generated due to Session Expired"
            response = unauthorized(error=self.error, data=token)
            response = JsonResponse(response, status=status.HTTP_401_UNAUTHORIZED)
            unify_printer(level=UNIFY_ERROR, message=f"Timeout ERROR", error=ex, traceback=traceback.format_exc())
        except Exception as ex:
            message = f"Exception occurred while validate token"
            unify_printer(level=UNIFY_ERROR, message=message, error=ex,
                          traceback=traceback.format_exc())
            response = internal_server_response(message, traceback.format_exc())
            response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        unify_audit_printer(request, response, start, time.time())
        logs = insert_unify_log()
        res = json.loads(response.getvalue().decode())
        res['log'] = logs
        response = JsonResponse(res, status=response.status_code)
        UserDetails.clear_user_details(UserDetails)
        return response

    def process_response(self, request, response):
        pass

    def verify_token(self, token):
        try:
            is_valid = False
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            is_valid = True
        except jwt.ExpiredSignatureError as ex:
            raise jwt.ExpiredSignatureError("Session Expired due to timeout")
        except jwt.InvalidSignatureError or jwt.InvalidTokenError as ex:
            self.error = "Invalid Session"
        except Exception as ex:
            unify_printer(level=UNIFY_ERROR, message=f"Exception occured while verify token", error=ex,
                          traceback=traceback.format_exc())
            self.error = "Authentication failed"
        return is_valid
