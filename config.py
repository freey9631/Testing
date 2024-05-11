import re
import os

id_pattern = re.compile(r'^.\d+$')

# Pyrogram client config
API_ID = os.environ.get("API_ID", "")
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
ADMINS = []

# Parsing admin IDs from environment variable and validating
for x in os.environ.get("ADMINS", "").split():
    try:
        ADMINS.append(int(x))
    except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

# Database config
DB_NAME = os.environ.get("DB_NAME", "Cluster0")
DB_URL = os.environ.get("DB_URL", "")
