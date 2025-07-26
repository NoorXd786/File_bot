# config.py

import os

OWNER_ID = int(os.getenv("OWNER_ID"))
BOT_TOKENS = os.getenv("BOT_TOKENS").split(",")  # Comma-separated if multiple
PRIVATE_CHANNEL_ID = os.getenv("PRIVATE_CHANNEL_ID")
