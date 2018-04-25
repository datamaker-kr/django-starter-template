try:
    from .settings_extra import IS_PRODUCTION
    is_production = IS_PRODUCTION
except ImportError:
    is_production = False

if is_production:
    from .production import *
else:
    from .development import *

try:
    from .settings_extra import *
except ImportError:
    pass
