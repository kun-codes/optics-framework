assert_equality
- nothing implemented for this in `optics_framework/api/verifier.py`

assert_presence
- each log line in `execution_logs.log` is printed twice and 4 times in some cases
- when tested with a text string and rule of "any", the screenshot shows with a green bordered box that text has been found but the tui still shows an E0401 error code
- when tested with an xpath, the result is not found despite the element being present on screen. Gives an E0201 error

capture_pagesource
- no xml is written to disk
- no logs are written in either `execution_logs.log` or `internal_logs.log`

capture_screenshot
- no screenshot is written to disk
- logs are printed twice in `execution_logs.log`

clear_element
- error code E0401 is thrown even if element is present on screen when passing element as text string, the text field is cleared despite the error code
- error code E0201 is thrown when element passed as string is not present on screen
- error code E0201 is thrown when element passed as xpath is present on screen. Text field is not cleared
- same as above when element is passed as an xpath but not present on screen
- in all above cases, logs are printed twice in `execution_logs.log`

close_and_terminate_app
- "INFO - No events to send." log printed twice in `execution_logs.log`
- app is correctly closed and terminated

condition
- TODO

date_evaluate
- `date_evaluate ${tomorrow} 04/28/2026 "+1 day"` gives the error "[E0901] Named element 'tomorrow3' is not defined in this project's elements". This is because despite `date_evaluate()` in `optics_framework/api/flow_control.py` having `@raw_params(0)` decorator, line 667 in `optics_framework/api/live.py` evaluates all the paramters
- `date_evaluate tomorrow5 04/28/2026 "+1 day"` gives the warning "[EVALUATE] Expected param1 in format '${name}', got 'tomorrow5'. Using as is." in `internal_logs.log` but the value is evaluated correctly. I verified it through the `/elements` command in the tui. The warning is printed twice though.

detect_and_press
- when passing element as a text string when it is on screen, the element is detected and pressed but an E0401 error code is thrown. No logs are printed in `execution_logs.log` or `internal_logs.log`. A `NoSuchElementError` is thrown followed by a "Pressing element" log in `internal_logs.log`.
- Same behavior occurs when the element is not on screen but obviously nothing is pressed and no logs saying "Pressing element" appears. Instead, logs "Timeout reached. Rule: any, Elements: ", "Validate Screen: Elements not found. Error: Code.E0201: ['element text'] not found based on rule 'any'." and "Element element text not found. Press is not performed." is printed twice for each in `internal_logs.log`
- when passing element as an xpath when it is on screen, the element is not detected and hence a press is not performed. `internal_logs.log` show a error `E0201` while `execution_logs.log` show that the element is not found. Logs are printed twice in both `execution_logs.log` and `internal_logs.log`. The TUI shows success with a green checkmark text
- when passing an element as an xpath when it is not on screen, same happens as the above point

enter_number
- TODO

enter_text
- when passing element as a text string when it is on screen, the element is detected and text is entered but an E0401 error code is thrown. No logs are printed in `execution_logs.log` or `internal_logs.log`. A `NoSuchElementError` is thrown followed by a "Entering text into element" log in `internal_logs.log`.
