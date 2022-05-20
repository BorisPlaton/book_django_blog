from django.conf import settings
from django.core.mail import send_mail


def share_post_via_email(data: dict):
    subject = f"{data['name']} ({data['email']}) recommends you reading \"{data['post_title']}\""
    message = f"Read \"{data['post_title']}\" at {data['post_url']}\n\n" \
              f"{data['name']}\'s comments: {data['comments']}"
    status = send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [data['to']],
    )

    return bool(status)
