from polyaxon.utils import config, ROOT_DIR

LIST_TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.template.context_processors.debug',
    'django.template.context_processors.i18n',
    'django.template.context_processors.media',
    'django.template.context_processors.static',
    'django.template.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'versions.context_processors.versions',
    'commands.context_processors.cluster',
    'sso.context_processors.sso_enabled',
]

JS_DEBUG = config.get_boolean('POLYAXON_JS_DEBUG')
DEBUG = config.get_boolean('POLYAXON_DEBUG')

if JS_DEBUG:
    def js_debug_processor(request):
        return {'js_debug': True}

    LIST_TEMPLATE_CONTEXT_PROCESSORS += ('polyaxon.settings.js_debug_processor',)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            ROOT_DIR.child('polyaxon').child('polyaxon').child('templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': config.get_boolean('DJANGO_TEMPLATE_DEBUG', is_optional=True) or DEBUG,
            'context_processors': LIST_TEMPLATE_CONTEXT_PROCESSORS,
        },
    },
]
