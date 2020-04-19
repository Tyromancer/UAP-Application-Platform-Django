from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """A class used for generating tokens used in the link included in
    Account Activation emails
    """
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.uapuser.email_confirmed)
        )


account_activation_token = AccountActivationTokenGenerator()
