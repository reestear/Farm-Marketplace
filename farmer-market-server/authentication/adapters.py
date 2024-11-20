from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_url(self, request, emailconfirmation):
        host = "localhost"
        protocol = "http"
        return f"{protocol}://{host}/api/auth/accounts/confirm-email/{emailconfirmation.key}/"
