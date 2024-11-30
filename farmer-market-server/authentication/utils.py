import re

from django.conf import settings


def replace_url_domain(url: str) -> str:
    """
    Replace the word between '//' and the next '/' in a URL with a new word.

    Args:
        url (str): The original URL.
        new_word (str): The word to replace with.

    Returns:
        str: The modified URL with the replaced word.
    """
    return re.sub(r"//([^/]+)/", f"//{settings.APPLICATION_HOST}/", url)


def extract_uid_and_token(url):
    # Regular expression to capture the UID and token in the URL
    pattern = (
        r"/password/reset/confirm/(?P<uid>[a-zA-Z0-9]+)/(?P<token>[a-zA-Z0-9\-]+)/?$"
    )
    match = re.search(pattern, url)

    if match:
        uid = match.group("uid")
        token = match.group("token")
        return uid, token
    else:
        raise ValueError("Invalid URL format or unable to extract UID and token.")
