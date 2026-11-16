"""Tests for AppManagement — a thin delegation layer over the driver."""
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest

from optics_framework.api.app_management import AppManagement
from optics_framework.common.config_handler import Config
from optics_framework.common.error import Code, OpticsError


@pytest.fixture
def app_management(mock_driver):
    builder = SimpleNamespace(get_driver=lambda: mock_driver, session_config=Config())
    return AppManagement(builder)


class TestAppManagement:
    def test_init_tolerates_missing_driver(self):
        # A None driver is logged, not raised, at construction time.
        AppManagement(SimpleNamespace(get_driver=lambda: None, session_config=Config()))

    def test_initialise_setup_is_noop(self, app_management):
        assert app_management.initialise_setup() is None

    @pytest.mark.parametrize(
        "method, args, kwargs, driver_attr, expected_args, expected_kwargs",
        [
            ("launch_app", (), {"app_identifier": "com.x"}, "launch_app", (),
             {"app_identifier": "com.x", "app_activity": None, "event_name": None}),
            ("launch_other_app", ("com.y", "ev"), {}, "launch_other_app", (),
             {"app_name": "com.y", "event_name": "ev"}),
            ("close_and_terminate_app", (), {}, "terminate", (), {}),
            ("force_terminate_app", ("com.z", "ev"), {}, "force_terminate_app", (),
             {"app_name": "com.z", "event_name": "ev"}),
            ("start_appium_session", (), {"event_name": "ev"}, "launch_app", (), {"event_name": "ev"}),
            ("get_driver_session_id", (), {}, "get_driver_session_id", (), {}),
        ],
    )
    def test_delegates_to_driver(self, app_management, mock_driver, method, args, kwargs,
                                 driver_attr, expected_args, expected_kwargs):
        getattr(app_management, method)(*args, **kwargs)
        getattr(mock_driver, driver_attr).assert_called_once_with(*expected_args, **expected_kwargs)

    def test_launch_app_returns_driver_result(self, app_management, mock_driver):
        mock_driver.launch_app.return_value = "session-123"
        assert app_management.launch_app(app_identifier="com.x") == "session-123"

    def test_get_app_version_without_package(self, app_management, mock_driver):
        mock_driver.get_app_version.return_value = "1.2.3"
        assert app_management.get_app_version() == "1.2.3"
        mock_driver.get_app_version.assert_called_once_with()

    def test_get_app_version_with_package(self, app_management, mock_driver):
        mock_driver.get_app_version.return_value = "4.5.6"
        assert app_management.get_app_version("com.x") == "4.5.6"
        mock_driver.get_app_version.assert_called_once_with(app_package="com.x")


class TestLaunchFromHomeScreen:
    @pytest.fixture
    def phone(self):
        return SimpleNamespace(LAUNCHES_FROM_HOME_SCREEN=True, app_targets=["app.png", "My App"], show_home_screen=Mock())

    @pytest.fixture
    def presser(self):
        with patch("optics_framework.api.app_management.ActionKeyword") as keyword:
            yield keyword.return_value

    @pytest.fixture
    def app_management(self, phone):
        driver = SimpleNamespace(active_instance=phone, show_home_screen=phone.show_home_screen)
        return AppManagement(SimpleNamespace(get_driver=lambda: driver, session_config=Config()))

    def test_launch_other_app_shows_the_home_screen_then_presses_the_name(self, app_management, phone, presser):
        app_management.launch_other_app("My App", "ev")
        phone.show_home_screen.assert_called_once_with()
        presser.press_element.assert_called_once_with("My App", event_name="ev")

    def test_launch_app_presses_the_icon_first(self, app_management, presser):
        app_management.launch_app()
        presser.press_element.assert_called_once_with("app.png", event_name=None)

    def test_launch_app_falls_back_to_the_name_from_the_home_screen_again(self, app_management, phone, presser):
        presser.press_element.side_effect = [OpticsError(Code.E0201), None]
        app_management.launch_app()
        assert [call.args[0] for call in presser.press_element.call_args_list] == ["app.png", "My App"]
        assert phone.show_home_screen.call_count == 2

    def test_launch_app_raises_the_last_error_when_nothing_is_found(self, app_management, presser):
        presser.press_element.side_effect = OpticsError(Code.E0201)
        with pytest.raises(OpticsError) as raised:
            app_management.launch_app()
        assert raised.value.code == Code.E0201

    def test_launch_app_without_a_target_is_a_config_error(self, app_management, phone, presser):
        phone.app_targets = []
        with pytest.raises(OpticsError) as raised:
            app_management.launch_app()
        assert raised.value.code == Code.E0503
        phone.show_home_screen.assert_not_called()
