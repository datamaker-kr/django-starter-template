from .base import *  # noqa : F403
import contextlib

if env('ENVIRONMENT') == 'development':  # noqa : F405
    from .development import *  # noqa : F403
elif env('ENVIRONMENT') == 'production':  # noqa : F405
    from .production import *  # noqa : F403
elif env('ENVIRONMENT') == 'local':  # noqa : F405
    with contextlib.suppress(ImportError):
        from .local import *  # noqa : F403
