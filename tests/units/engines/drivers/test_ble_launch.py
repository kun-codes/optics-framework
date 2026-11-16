from unittest.mock import MagicMock, patch

import pytest

pytest.importorskip("serial")

from optics_framework.engines.drivers import ble  # noqa: E402
from optics_framework.engines.drivers.ble import BLEDriver  # noqa: E402

CAPABILITIES = {"device_id": "phone", "port": "/dev/ttyFAKE", "pixel_width": 1080, "pixel_height": 2400,
                "mickeys_width": 385, "mickeys_height": 855}


def driver(**capabilities):
    with patch.object(ble, "Serial") as serial:
        instance = BLEDriver(config={"capabilities": {**CAPABILITIES, **capabilities}}, event_sdk=MagicMock())
    instance.ser = serial.return_value
    instance.ser.write.reset_mock()
    return instance


def lines(instance):
    return [call.args[0].decode().strip() for call in instance.ser.write.call_args_list]


@pytest.fixture(autouse=True)
def no_sleep():
    with patch.object(ble.time, "sleep") as sleep:
        yield sleep


def test_the_home_screen_is_shown_by_pressing_home_then_back_and_waiting_after_each(no_sleep):
    phone = driver(home_delay=2.5)
    no_sleep.reset_mock()
    phone.show_home_screen()
    assert lines(phone) == [str(BLEDriver.CONSUMER_HOME), "0", str(BLEDriver.CONSUMER_BACK), "0"]
    assert [call.args[0] for call in no_sleep.call_args_list if call.args[0] == 2.5] == [2.5, 2.5]


@pytest.mark.parametrize("capabilities, targets", [
    ({"app_icon": "app.png", "app_name": "My App"}, ["app.png", "My App"]),
    ({"app_name": "My App"}, ["My App"]),
    ({}, []),
])
def test_the_targets_are_the_icon_then_the_name_and_none_left_out(capabilities, targets):
    assert driver(**capabilities).app_targets == targets


@pytest.mark.parametrize("launch", ["launch_app", "launch_other_app"])
def test_the_driver_itself_cannot_launch_because_it_has_no_eyes(launch):
    phone = driver()
    args = ("My App",) if launch == "launch_other_app" else ()
    with pytest.raises(NotImplementedError, match="home screen"):
        getattr(phone, launch)(*args)
    assert lines(phone) == []
