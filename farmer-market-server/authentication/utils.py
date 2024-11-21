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
