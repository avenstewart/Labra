import pytest
from labra.tasks.api.callsign_endpoint import CallsignEndpointTasks

@pytest.mark.api
@pytest.mark.smoke
def test_callsign_endpoint(api_context, base_config, callsigns):
    callsign_endpoint = CallsignEndpointTasks(api_context, base_config, callsigns)

    callsign_endpoint.verify_valid_callsign()
    callsign_endpoint.verify_invalid_callsign()
    callsign_endpoint.verify_license_type()
