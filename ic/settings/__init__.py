# settings.py
import os

# Default config between dev and prd
# export SITE_ENV =  'production'
ENV = os.environ.get('SITE_ENV', None)
if ENV == 'production':
    from .prod import *
elif ENV == 'development':
    from .dev import *
else:
    from .dev import *
