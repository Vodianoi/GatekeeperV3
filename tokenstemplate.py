import os

# Discord Server Connection Bot Token (Under Bot request token)
token = os.getenv('DISCORD_BOT_TOKEN', 'IGNORE THIS FIELD IF TESTING AMP/DB')

# 2Factor AUTH Code for AMP Console Login
AMPAuth = os.getenv('AMP_AUTH', '')

# Login creds - ## DO NOT SHARE! ##
AMPUser = os.getenv('AMP_USER', '')
AMPPassword = os.getenv('AMP_PASSWORD', '')
AMPurl = os.getenv('AMP_URL', '')

