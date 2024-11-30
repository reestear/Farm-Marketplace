from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

from .utils import extract_uid_and_token


class CustomAccountAdapter(DefaultAccountAdapter):

    def send_mail(self, template_prefix, email, context):
        if "password_reset_url" in context:
            uid, token = extract_uid_and_token(context["password_reset_url"])

            context["password_reset_url"] = (
                settings.PASSWORD_RESET_REDIRECT_URL + f"?uid={uid}&token={token}"
            )
        super().send_mail(template_prefix, email, context)
