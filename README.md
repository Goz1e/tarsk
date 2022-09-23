# tarsk

dependencies : django_on_heroku, django_phone_numbers, crispy_forms, crispy-bootstrap5

pip install django-crispy-forms django-phonenumber-field[phonenumbers] crispy-bootstrap5




# add the following to settings.installed_apps 
INSTALLED_APPS = [
    'phonenumber_field',
    'crispy_forms',
    'crispy_bootstrap5',
]


# bottom of setting.py
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

# if you are hosting on heroku 
pip install django_on_heroku
add 'django_on_heroku' to settings.installed_apps

