from unittest.mock import MagicMock, patch

import pytest

pytest.importorskip("serial")

from optics_framework.engines.drivers import ble  # noqa: E402
from optics_framework.engines.drivers.ble import BLEDriver  # noqa: E402

CAPABILITIES = {"device_id": "phone", "port": "/dev/ttyFAKE", "pixel_width": 1080, "pixel_height": 2400,
                "mickeys_width": 385, "mickeys_height": 855}


def driver():
    with patch.object(ble, "Serial") as serial:
        instance = BLEDriver(config={"capabilities": CAPABILITIES}, event_sdk=MagicMock())
    instance.ser = serial.return_value
    instance.ser.write.reset_mock()
    return instance


def lines(instance):
    return [call.args[0].decode().strip() for call in instance.ser.write.call_args_list]


@pytest.fixture(autouse=True)
def no_sleep():
    with patch.object(ble.time, "sleep"):
        yield


def test_go_home_presses_ac_home_then_releases_it():
    phone = driver()
    phone.go_home()
    assert lines(phone) == ["547", "0"]


def test_go_back_presses_ac_back_then_releases_it():
    phone = driver()
    phone.go_back()
    assert lines(phone) == ["548", "0"]


def test_the_event_is_captured_once_before_the_key():
    phone = driver()
    phone.go_home(event_name="home")
    phone.event_sdk.capture_event.assert_called_once_with("home")
