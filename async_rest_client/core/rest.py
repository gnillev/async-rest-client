from concurrent.futures import ThreadPoolExecutor, Future
import functools
from typing import Optional

import requests


class Rest:
    """
    Basic REST client
    """
    
    def __init__(self, url: Optional[str]):
        self.url = url
        self.pool = ThreadPoolExecutor(thread_name_prefix="request")

    def request(self, endpoint: str) -> str:
        sep = "/" if not self.url.endswith("/") else ""
        url = f"{self.url}{sep}{endpoint}"
        response = requests.get(url)
        return response.json()

    def async_request(self, endpoint: str) -> Future:
        response_future = self.pool.submit(self.request, endpoint)
        return response_future
