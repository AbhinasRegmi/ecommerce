from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
#we will be creating token for account activation/verification

class AccountVerificationTokenGenerator(PasswordResetTokenGenerator):
    
    def _make_hash_value(self, user, timestamp):
        return {
            text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)
        }


account_verfication_token = AccountVerificationTokenGenerator()