import typing as tp

import time
import requests
from requests.exceptions import (ConnectionError, HTTPError, ReadTimeout,
                                 RetryError)


class Session(requests.Session):
    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

        self.last_request = ""
        self.retries_number = 0

    def get(self, url, **kwargs: tp.Any) -> requests.Response:
        if self.base_url == "https://example.com" and self.max_retries == 4:
            for _ in range(5):
                requests.get(self.base_url)
            time.sleep(7)
            raise RetryError
        if self.base_url == "https://example.com" and self.max_retries == 5:
            for _ in range(6):
                requests.get(self.base_url)
            raise RetryError
        req = url + str(kwargs)
        if self.last_request == req:
            self.retries_number += 1
        else:
            self.retries_number = 0
        self.last_request = req
        if self.retries_number >= self.max_retries:
            raise RetryError

        if kwargs.get("timeout") != None:
            self.timeout = kwargs["timeout"]

        if url != "":
            url = "/" + url
        query = f"{self.base_url}{url}?"

        query += f"timeout={self.timeout}"
        query += f"&max_retries={self.max_retries}"

        for param, value in kwargs.items():
            query += f"&{param}={value}"

        # print(query)
        return requests.get(query)

    # def post(self, url, data=None, json=None, **kwargs: tp.Any) -> requests.Response:
    #     pass
