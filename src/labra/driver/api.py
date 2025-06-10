# src/labra/drivers/api_driver.py
import requests
from labra.drivers.base import BaseDriver

class ApiDriver(BaseDriver):
    """
    Driver for interacting with HTTP-based APIs.
    Suitable for RESTful or JSON-over-HTTP test scenarios.
    """

    def __init__(self, config):
        super().__init__(config)
        self.base_url = config.get("base_url", "http://localhost:8000")
        self.headers = config.get("headers", {})
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def setup(self):
        print(f"[ApiDriver] Initialized for: {self.base_url}")

    def execute(self, command_or_payload):
        """
        Sends an HTTP request.

        Args:
            command_or_payload (dict): A dictionary with keys like method, endpoint, params, data, json

        Returns:
            requests.Response: The response object
        """
        if not isinstance(command_or_payload, dict):
            raise ValueError("ApiDriver expects a dict with method and endpoint")

        method = command_or_payload.get("method", "GET").upper()
        endpoint = command_or_payload.get("endpoint", "/")
        url = self.base_url.rstrip("/") + "/" + endpoint.lstrip("/")

        response = self.session.request(
            method=method,
            url=url,
            params=command_or_payload.get("params"),
            data=command_or_payload.get("data"),
            json=command_or_payload.get("json")
        )

        return response

    def teardown(self):
        self.session.close()
        print("[ApiDriver] Session closed.")
