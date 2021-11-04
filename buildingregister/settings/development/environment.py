from split_settings.tools import optional, include

DEBUG=True

include(
    '../common/*.py',
    'database.py',
    'security.py',
)

