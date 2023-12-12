from urllib import request


def get_html_page(url: str) -> bytes:
    with request.urlopen(url) as f:
        return f.read()
