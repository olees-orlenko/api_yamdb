from datetime import datetime
import re

from django.core.exceptions import ValidationError
from rest_framework import serializers


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError(f'Недопустипое имя - {value}!')
    if re.search(r'^[-a-zA-Z0-9_]+$', value) is None:
        raise ValidationError('Недопустимые символы')


def validate_score(score):
    if 1 > score > 10:
        raise serializers.ValidationError(
            'Оценка должна быть от 1 до 10')
    return score


def validate_year(value):
    current_year = datetime.today().year
    if value > current_year:
        raise serializers.ValidationError('Проверьте год выхода!')
    return value
