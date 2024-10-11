import os

from dotenv import load_dotenv

load_dotenv()

if os.getenv("ENV_NAME") == "PROD":
    from .prod import *
else:
    from .dev import *
