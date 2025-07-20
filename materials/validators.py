from rest_framework.serializers import ValidationError


def validate_youtube_url(value):
    """
    Разрешает только ссылки на YouTube.
    """
    if 'youtube.com' not in value and 'youtu.be' not in value:
        raise ValidationError('Разрешены только ссылки на YouTube.')
    return value