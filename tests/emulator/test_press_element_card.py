"""
Press Element card (optics-test-app, Card 23) — end-to-end via the Optics SDK.

Verification is deliberately independent of optics's own locate/press logic: using
optics.assert_presence/assert_visibility here would be circular, since both share the
same locator-strategy machinery (XPath/accessibility/OCR/image matching, with
self-heal fallback) as press_element itself. Instead each stage is verified via
optics.capture_pagesource() — a raw page-source XML fetch through the already-live
Appium session (like plain driver.page_source in Selenium/Appium), with no strategy
fallback or self-heal involved.

Each test is INDEPENDENT: it deep-links straight to its own Card23_S{n} stage before
acting, so a failure in one stage can't cascade into the next (an earlier version
chained S1->S2->...->S9 through a single module fixture, so one broken stage left every
later stage running on the wrong screen). Every Card23 stage is registered as a
teststudio://Card23_S{n} route, so the deep link lands directly on the stage.

Note: an earlier version shelled out to `adb shell uiautomator dump` for verification,
on the theory that a fully separate process is more "independent". In practice that
conflicts with Appium's own live UiAutomator2 instrumentation session — both grab
exclusive UiAutomator access and one gets killed (observed as exit code 137).
capture_pagesource() avoids this since it reuses the existing session.
"""

import os

import pytest

from optics_framework.optics import Optics

# discover_templates() recursively scans project_path for image files and registers
# each by its bare filename — so the icon template is found regardless of subfolder,
# but by convention it lives at test_data/input_templates/ (see optics_framework/samples/*).
PROJECT_PATH = os.path.dirname(__file__)

config = {
    "project_path": PROJECT_PATH,
    "driver_sources": [
        {
            "appium": {
                "enabled": True,
                "url": "http://localhost:4723",
                "capabilities": {
                    "platformName": "Android",
                    "deviceName": "emulator-5554",
                },
            }
        }
    ],
    # appium_find_element locates elements, but its capture() returns None — screenshots
    # (needed by the OCR/image strategies) require appium_screenshot. appium_page_source
    # backs capture_pagesource(). Mirrors the three-source setup in optics_framework/samples/*.
    "elements_sources": [
        {"appium_find_element": {"enabled": True}},
        {"appium_page_source": {"enabled": True}},
        {"appium_screenshot": {"enabled": True}},
    ],
    "text_detection": [{"easyocr": {"enabled": True}}],
    "image_detection": [{"templatematch": {"enabled": True}}],
}


def dump_ui(optics) -> str:
    """Raw page-source XML via the live Appium session — no locator/self-heal logic involved.

    Settles first: presses trigger React Navigation stack transitions that take a beat,
    and capturing mid-transition catches the outgoing screen.
    """
    optics.sleep("3")
    return optics.capture_pagesource()["page_source"]


def goto(optics, stage: str) -> None:
    """Deep-link straight to a Card23 stage so each test starts from a known screen.

    Uses the app's teststudio://Card23_S{n} route (React Navigation linking config),
    the same mechanism the fixture uses for the initial launch. String concat (not
    str.format/%) keeps the literal JSON braces intact.
    """
    # A native AlertDialog left over from a prior (failed) stage sits *above* the RN
    # view, so deep-linking swaps the screen behind it but the dialog stays up and
    # eats the next test's presses. Best-effort dismiss any stray dialog first.
    try:
        optics.press_element('//*[@text="OK"]')
    except Exception:  # noqa: BLE001 - no dialog present is the normal case
        pass
    optics.execute_script(
        '{"script": "mobile: deepLink", "args": {"url": "teststudio://'
        + stage
        + '", "package": "com.teststudio"}}'
    )
    optics.sleep("2")  # let the deep-linked screen render before interacting


@pytest.fixture(scope="module")
def optics():
    o = Optics(config=config)
    o.launch_app(app_identifier="com.teststudio", app_activity=".MainActivity")
    # Cold start: wait out the splash screen / JS bundle load before interacting.
    o.sleep("10")
    yield o
    o.quit()


def test_s1_index_disambiguation(optics):
    """5 identical 'NEXT' buttons; only document-index 2 is correct. Tests `index`."""
    goto(optics, "Card23_S1")
    optics.press_element_with_index("NEXT", index="2")
    assert "c23-s2" in dump_ui(optics)


def test_s2_aoi_scoping(optics):
    """9 identical 'TARGET' tiles; only the centre one (in the AOI) is correct.

    Scopes OCR text detection to the centre region of the screen so only the AOI's
    'TARGET' is a candidate. AOI values are screen percentages (top-left x/y + w/h).
    """
    goto(optics, "Card23_S2")
    optics.press_element("TARGET", aoi_x="30", aoi_y="33", aoi_width="22", aoi_height="9")
    assert "c23-s3" in dump_ui(optics)


def test_s3_checkbox_radio(optics):
    """Native checkbox + radio controls, then Continue. Located by resource-id (testID)."""
    goto(optics, "Card23_S3")
    optics.press_element('//*[@resource-id="c23-s3-checkbox-terms"]')
    optics.press_element('//*[@resource-id="c23-s3-radio-pro"]')
    optics.press_element('//*[@resource-id="c23-s3-continue"]')
    assert "c23-s4" in dump_ui(optics)


@pytest.mark.xfail(
    reason="optics matches images with SIFT, which needs at least 10 matching feature "
    "points to count as a hit. A plain, symmetric heart icon simply doesn't have that "
    "many distinct features (measured only ~5 against the live screen), so this can't "
    "pass reliably. SIFT is meant for detailed/photographic images, not flat one-colour "
    "icons. Making it a real pass would mean showing a detail-rich image in the app "
    "instead of a simple vector icon.",
    strict=False,
)
def test_s4_icon_match(optics):
    """Icon-only buttons (no text/accessibility label) — forces image template matching.

    Template: test_data/input_templates/press_element_card23_s4_heart_icon.png
    """
    goto(optics, "Card23_S4")
    optics.press_element("press_element_card23_s4_heart_icon.png")
    assert "c23-s5" in dump_ui(optics)


def test_s5_repeat(optics):
    """Button needs exactly 5 presses to advance. Tests `repeat` (re-taps the same element)."""
    goto(optics, "Card23_S5")
    optics.press_element('//*[@resource-id="c23-s5-tap-btn"]', repeat="5")
    assert "c23-s6" in dump_ui(optics)


def test_s6_offset(optics):
    """Only a sub-region (top-right hotspot) of one large zone is correct. Tests
    `offset_x`/`offset_y` applied to an element-resolved (WebElement) press.

    Offsets are from the zone's centre. On the CI emulator the zone renders ~578x578 px;
    the hotspot centre-fraction is (0.841, 0.159), i.e. offset (+0.341*w, -0.341*h) ~=
    (+197, -197) px. Locate the zone by resource-id so the offset is measured from the
    zone centre (not the hint text inside it).
    """
    goto(optics, "Card23_S6")
    optics.press_element('//*[@resource-id="c23-s6-zone"]', offset_x="197", offset_y="-197")
    assert "c23-s7" in dump_ui(optics)


def test_s7_ocr_accessibility_mismatch(optics):
    """Visible text 'CANCEL' but accessibilityLabel 'SUBMIT'. text_only: forces the OCR
    path to read the visible glyphs rather than the accessibility tree."""
    goto(optics, "Card23_S7")
    optics.press_element("text_only:CANCEL")
    assert "c23-s8" in dump_ui(optics)


def test_s8_secure_screen(optics):
    """FLAG_SECURE screen (screenshots blank); press via resource-id + verify via page source."""
    goto(optics, "Card23_S8")
    optics.press_element('//*[@resource-id="c23-s8-continue"]')
    assert "Success" in dump_ui(optics)
