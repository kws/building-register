import logging

from register.models import SignInRecord, ContactDetails
from register.util.tokens import get_token_method

logger = logging.getLogger(__name__)


def send_reminders(send=False, template="reminder"):
    signed_in = SignInRecord.objects.today().open().values("user")
    detail_query = ContactDetails.objects.filter(user__in=signed_in, audit__isnull=False)

    for detail in detail_query:
        if send:
            try:
                method = get_token_method(detail.method)
                method.send_message(detail.value, template)
            except:
                logger.exception(f"Could not send reminder to: {detail}")
        else:
            print(detail)

