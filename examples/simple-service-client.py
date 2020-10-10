
from concurrent.futures import as_completed
from time import time
from typing import Iterator, Optional

from async_rest_client.core.rest import Rest


class SimpleServiceClient(Rest):

    def __init__(self, url: Optional[str] = None):
        url = url or "http://localhost:8000/"
        super().__init__(
            url=url
        )
    
    def wait_and_echo(self, echo_string: str) -> str:
        return self.request(f"wait/{echo_string}")

    def async_wait_and_echo(self, echo_string: str) -> str:
        return self.async_request(f"wait/{echo_string}")

    def yield_wait_and_echo_requests(self) -> Iterator[str]:
        responses = [self.async_wait_and_echo(str(i)) for i in range(10)]
        return as_completed(responses)

            


if __name__ == "__main__":
    client = SimpleServiceClient()
    start = time()
    response_generator = client.yield_wait_and_echo_requests()
    results = [future.result() for future in response_generator]
    end = time()
    delta = end-start
    tot_waited = sum(result['waited'] for result in results)
    print(f"Actual: {delta}")
    print(f"Server wait: {tot_waited}")
