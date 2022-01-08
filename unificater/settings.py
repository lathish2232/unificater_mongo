import os
from decouple import config, Csv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '-w!8wtyyzlur@os_q7-w8#jb$19c#pmd($jktp!$ws1*v#%i(u'
# JWT PROPERTIES
SECRET_KEY = config('SECRET_KEY', default='-w!8wtyyzlur@os_q7-w8#jb$19c#pmd($jktp!$ws1*v#%i(u')
DEBUG = config('DEBUG', default=False, cast=bool)
ALGORITHM = config('JWT_ALGORITHM', default='HS256')
TOKEN_HEADER = config('JWT_TOKEN_HEADER', default='Authorization')
JWT_AGE = config('JWT_AGE', default=32400, cast=int)  # 9 Hour
RESET_KEY_EXP = config('RESET_KEY_EXP', default=15, cast=int)
AUTH_EXCLUDE = config('AUTH_EXCLUDE', cast=Csv())
RESET_PSWD_LINK = config('RESET_PSWD_LINK', default='http://localhost:3000/auth/reset-password')

# ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
# CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = config('CORS_ORIGIN_ALLOW_ALL', default=False, cast=bool)
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', cast=Csv())
CORS_ALLOW_HEADERS = config('CORS_ALLOW_HEADERS', cast=Csv())
CORS_ALLOW_METHODS = config('CORS_ALLOW_METHODS', cast=Csv())
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=1, cast=int)
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=True, cast=bool)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True, cast=bool)

# Application definition
LANGUAGE_CODE = config('LANGUAGE_CODE', default='en-us')
TIME_ZONE = config('TIME_ZONE', default='UTC')
USE_I18N = config('USE_I18N', default=True, cast=bool)
USE_L10N = config('USE_L10N', default=True, cast=bool)
USE_TZ = config('USE_L10N', default=True, cast=bool)
FILE_LOGGER = config('FILE_LOGGER', default=False, cast=bool)

# DB
DB_HOST = config('DB_HOST', default='127.0.0.1')
DB_PORT = config('DB_PORT', default='27017')
DATABASE = config('DATABASE', default='unificaterFlows')
IS_AUTH_ENABLE = config('IS_AUTH_ENABLE', default=False, cast=bool)
AUTH_DB = config('AUTH_DB', default='')
AUTH_DB_USER = config('AUTH_DB_USER', default='')
AUTH_DB_PASS = config('AUTH_DB_PASS', default='')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
ROOT_URLCONF = 'unificater.urls'
WSGI_APPLICATION = 'unificater.wsgi.application'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  # required for serving swagger ui's css/js files
    'corsheaders',
    'django_extensions',
    'drf_yasg',
    'rest_framework',
    'service',
    'users'

]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'service.middleware.TokenValidation',
]

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'service.util.exception.unify_exception_handler'
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.dirname(os.getcwd())],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
            # 'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'verbose': {
            # 'format': '{"time": "%(asctime)s", "level": "%(levelname)s", "name": "%(name)s", "path": "%(pathname)s.%(funcName)s():%(lineno)d", "message": "%(message)s"}',
            'format': '[%(asctime)s] %(levelname)s [%(thread)d] [%(threadName)s] [%(name)s] %(message)s',
            # 'datefmt': '%Y-%m-%d %H:%M:%S.%s'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'development_logfile': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/unify_service.log',
            'maxBytes': 1024 * 1024 * 100,  # 100MB
            'backupCount': 10,
            'formatter': 'verbose'
        },
        'development_audit_logfile': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/unify_audit.log',
            'maxBytes': 1024 * 1024 * 100,  # 100MB
            'backupCount': 10,
            'formatter': 'verbose'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console'],
    },
    'loggers': {
        'py.warnings': {
            'handlers': ['development_logfile'],
            'propagate': True,
        },
        'service': {
            'handlers': ['development_logfile'],
        },
        'unify_service': {
            'handlers': ['development_logfile'],
        },
        'audit': {
            'handlers': ['development_audit_logfile'],
        },
        '': {
            'handlers': ['console', 'development_logfile'],
        },
    }
}

# MAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
