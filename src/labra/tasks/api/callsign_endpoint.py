from playwright.sync_api import APIRequestContext

class CallsignEndpointTasks:
    def __init__(self, request: APIRequestContext, base_config, callsigns):
        self.request = request
        self.base_url = base_config['base_url']
        self.callsigns = callsigns

    def verify_valid_callsign(self):
        test_data = self.callsigns["VALID"]
        callsign = test_data['callsign']

        response = self.request.get(f"{callsign}/json")
        assert response.status == 200, f"Callsign {callsign} not found"
        data = response.json()
        assert data.get("status") == "VALID", f"{callsign} expected to be VALID"
        return data

    def verify_invalid_callsign(self):
        test_data = self.callsigns["INVALID"]
        callsign = test_data['callsign']

        response = self.request.get(f"{callsign}/json")
        assert response.status == 200
        data = response.json()
        assert data.get("status") == "INVALID", f"{callsign} expected to be INVALID"
        return data

    def verify_license_type(self):
        test_data = self.callsigns["VALID"]
        callsign = test_data['callsign']
        callsign_type = test_data['type']

        response = self.request.get(f"{callsign}/json")
        assert response.status == 200
        data = response.json()
        actual_type = data.get("type", "").upper()
        assert actual_type == callsign_type, f"{callsign}: expected type {callsign_type}, got {actual_type}"
        return data