__title__ = "ftms_client"

import logging

from .client import Client

logging.getLogger(__name__).addHandler(logging.NullHandler())
