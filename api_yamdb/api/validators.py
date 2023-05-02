import re
from django.core.exceptions import ValidationError


def validate_username(value):
    if value == 'me':
        raise ValidationError(f'Недопустипое имя - {value}!')
    # if re.search(r'^[-a-zA-Z0-9_]+$', value) is None:
    #     raise ValidationError('Недопустимые символы')