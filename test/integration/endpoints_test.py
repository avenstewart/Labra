import pytest
from labra.tasks.api.callsign_endpoint import CallsignEndpointTasks

@pytest.mark.api
@pytest.mark.smoke
def test_callsign_endpoint(api_context, base_config, callsigns):
    callsigns = CallsignEndpointTasks(api_context, base_config, callsigns)

    callsigns.verify_valid_callsign()
    callsigns.verify_invalid_callsign()
    callsigns.verify_license_type()
