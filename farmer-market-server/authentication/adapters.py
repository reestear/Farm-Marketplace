from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

from .utils import replace_url_domain


class CustomAccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_url(self, request, emailconfirmation):
        host = settings.APPLICATION_HOST
        protocol = "http"
        return f"{protocol}://{host}/api/auth/accounts/confirm-email/{emailconfirmation.key}/"

    def send_mail(self, template_prefix, email, context):
        print("HEREWEGO: ", context, flush=True)

        if "password_reset_url" in context:
            context["password_reset_url"] = replace_url_domain(
                context["password_reset_url"]
            )
        super().send_mail(template_prefix, email, context)
