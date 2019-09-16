import settings


DEFAULT_SECRET_KEY = '1lRCqvUtnWaKkzrU'

SECRET_KEY = getattr(settings, 'SECRET_KEY', DEFAULT_SECRET_KEY)