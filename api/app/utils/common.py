import os


def generate_client_url(path: str, params: dict = None) -> str:
    url = os.getenv('CLIENT_URL') + path
    if params:
        return url + '?' + '&'.join([f"{k}={v}" for k, v in params.items()])
    return url
