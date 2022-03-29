from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings

import six
from random import choice
from string import digits

from apps.account.models import Account

SIZE = getattr(settings, "MAXIMUM_URL_CHARS", 6)
AVAIABLE_CHARS = digits


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: Account, timestamp: int):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

generate_token = TokenGenerator()

def create_random_code(chars=AVAIABLE_CHARS):
    """
    Creates a random string with the predetermined size
    """
    return "".join(
        [choice(chars) for _ in range(SIZE)]
    )