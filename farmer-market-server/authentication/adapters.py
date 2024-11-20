from allauth.account.adapter import DefaultAccountAdapter

from .utils import replace_url_domain

# from django.core.mail import EmailMultiAlternatives


class CustomAccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_url(self, request, emailconfirmation):
        host = "localhost"
        protocol = "http"
        return f"{protocol}://{host}/api/auth/accounts/confirm-email/{emailconfirmation.key}/"

    # def get_host(self, request):
    #     if request:
    #         return request.get_host()  # Dynamically get the host from the request
    #     return "defaultdomain.com"

    # def send_password_reset_mail(self, user, email, context):
    #     host = "localhost"  # Replace with your domain or use settings
    #     protocol = "http"  # Replace with "https" if applicable

    #     # Customize the password reset URL
    #     reset_url = f"{protocol}://{host}/api/auth/password/reset/confirm/{context['uid']}/{context['token']}/"
    #     context["password_reset_url"] = reset_url

    #     # Call the parent method to send the email with the modified context
    #     super().send_mail("account/email/password_reset_key", email, context)

    def send_mail(self, template_prefix, email, context):
        # print("HERE: ", context["password_reset_url"], flush=True)
        # # Example customization of email content
        # subject = "Custom Subject"
        # body = f"Hello, use this link: {context['password_reset_url']}"
        # email_message = EmailMultiAlternatives(subject, body, to=[email])
        # email_message.send()

        context["password_reset_url"] = replace_url_domain(
            context["password_reset_url"]
        )
        super().send_mail(template_prefix, email, context)
