from django.conf import settings
from django.core.mail import send_mail

from service.util.unify_logger import UNIFY_ERROR, unify_printer, UNIFY_DEBUG
from unificater.settings import RESET_KEY_EXP, RESET_PSWD_LINK


def send_reset_mail(to, reset_key):
    try:
        subject = 'Please reset your password'
        message = f'We heard that you have forgot your unificater account password.\n\n' \
                  f'Don\'t worry! You can use following link for reset your password.\n\n' \
                  f'{RESET_PSWD_LINK}/{reset_key}' \
                  f'\n\nNote: This link will be expired in {RESET_KEY_EXP} Minutes.' \
                  f'\n\n\nThanks,\n' \
                  f'Unificater team.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [to]
        result = send_mail(subject, message, email_from, recipient_list)
        unify_printer(level=UNIFY_DEBUG, message=f"Mail result: {result}")
    except Exception as ex:
        unify_printer(level=UNIFY_ERROR, message='Exception occurred while send reset link.',
                      error=ex, traceback=message)
