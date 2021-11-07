import os

SLACK_WEBHOOKS = os.environ.get('SLACK_SIGNIN_WEBHOOKS', '').split(' ')

