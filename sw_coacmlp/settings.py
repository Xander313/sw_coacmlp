
from pathlib import Path
from decouple import config
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'Aplicaciones/static')]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'ckeditor',
    'social_django',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Aplicaciones.Mision',
    'Aplicaciones.Vision',
    'Aplicaciones.Historia',
    'Aplicaciones.Noticias',
    'Aplicaciones.Objetivos',
    'Aplicaciones.Pregunta',
    'Aplicaciones.Progreso',
    'Aplicaciones.Testimonios',
    'Aplicaciones.Valores',
    'Aplicaciones.Educacion',
    'Aplicaciones.Capitulo',
    'Aplicaciones.Examen',
    'Aplicaciones.AdministrarEducacion',
    'Aplicaciones.Respuesta',
    'Aplicaciones.Autenticacion',
    'Aplicaciones.Contenido',
    'Aplicaciones.AdministrarContenido'


]


CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source']
        ],
        'height': '100%',
        'width': '100%',
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'Aplicaciones.Educacion.middlewares.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'sw_coacmlp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'Aplicaciones', 'templates'),
            os.path.join(BASE_DIR, 'Aplicaciones', 'AdministrarContenido', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',           
                'social_django.context_processors.login_redirect',      
            ],
        },
    },
]



WSGI_APPLICATION = 'sw_coacmlp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'sw_coacmlp.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es-ec'

TIME_ZONE = 'America/Guayaquil'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

X_FRAME_OPTIONS = 'ALLOWALL'


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)



SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')


LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/educacion/postlogin/'


SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid',
]

SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ['name', 'given_name', 'family_name', 'email', 'picture']


SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'Aplicaciones.Educacion.pipeline.prevent_account_conflict',  # Moved after social_user
    'Aplicaciones.Educacion.pipeline.get_user_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'Aplicaciones.Educacion.pipeline.guardar_visitante',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

# Asegúrate de tener estas configuraciones
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/educacion/postlogin/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/educacion/postlogin/'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/educacion/errorSesion/'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False

SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
    'prompt': 'select_account',
}

SOCIAL_AUTH_LOGIN_ERROR_URL = '/errorSesion/'


SOCIAL_AUTH_LOGIN_ERROR_URL = '/educacion/errorSesion/'
SOCIAL_AUTH_BACKEND_ERROR_URL = '/educacion/errorSesion/'
SOCIAL_AUTH_RAISE_EXCEPTIONS = DEBUG 



################################################
#####VARIABLES PARA LOS ADMINISTRADORES#########
################################################



USER_CONTENIDO = config("USER_CONTENIDO")
PASSWORD_CONTENIDO = config("PASSWORD_CONTENIDO")

USER_EDUCACION = config("USER_EDUCACION")
PASSWORD_EDUCACION = config("PASSWORD_EDUCACION")
