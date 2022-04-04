from .base import *

if env('ENVIRONMENT') == 'development':
    from .development import *
elif env('ENVIRONMENT') == 'production':
    from .production import *
elif env('ENVIRONMENT') == 'local':
    try:
        from .local import *
    except ImportError:
        pass
