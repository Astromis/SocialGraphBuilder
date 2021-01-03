from requests.adapters import HTTPAdapter
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


import requests

#https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/

DEFAULT_TIMEOUT = 5 # seconds

class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)

vk_api = requests.Session()

retry_strategy = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "OPTIONS", "POST"],
    backoff_factor=1
)
adapter = TimeoutHTTPAdapter(timeout=2.5, max_retries=retry_strategy)

vk_api.mount("https://", adapter)
vk_api.mount("http://", adapter)

response = http.get("https://en.wikipedia.org/w/api.php")