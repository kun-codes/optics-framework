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
- doesn't work
- can be fixed by using copying code structure from `enter_text()` in `action_keyword.py` to `enter_number()` in `action_keyword.py`

enter_text
- when passing element as a text string when it is on screen, the element is detected and text is entered but an E0401 error code is thrown. No logs are printed in `execution_logs.log` or `internal_logs.log`. A `NoSuchElementError` is thrown followed by a "Entering text into element" log in `internal_logs.log`.

## keywords after this were tested solely via `optics serve` command

enter_text_direct
- works

enter_text_using_keyboard
- doesn't work. Tried <enter> as written at https://mozarkai.github.io/optics-framework/usage/keyword_usage/#enter-text-using-keyboard and it instead typed "SpecialKey.ENTER" into the text field.

evaluate
- doesn't work. Tried:
  ```
  {
  "mode": "keyword",
  "keyword": "Evaluate",
  "params": ["${result}", "1 + 2 * 3"],
  "template_images": {}
  }
  ```

  Returned:
  ```
  {
  "detail": "Execution failed: All fallback attempts failed for keyword 'Evaluate':\n('${result}', '1 + 2 * 3') -> OpticsError('Code.E0701: Execution failed: Code.E0701: Execution failed: Code.E0401: Keyword execution failed: Code.E0702: Session elements is not an ElementData instance or is None.')"
  }
  ```
  
execute_module
- TODO

execute_script
- works, tested with 
    ```
    {
      "mode": "keyword",
      "keyword": "Execute Script",
      "params": [
        "{\"script\": \"mobile:pressKey\", \"args\": {\"keycode\": 3}}"
      ],
      "template_images": {}
    }
    ```

force_terminate_app
- works

get_app_version
- doesn't work. Tried with:
    ```
    {
        "mode": "keyword",
        "keyword": "Get App Version",
        "params": ["com.samsung.android.calendar"],
        "template_images": {}
    }
    ```

    got this:
    ```
    {
        "detail": "Execution failed: All fallback attempts failed for keyword 'Get App Version':\n('com.samsung.android.calendar',) -> OpticsError(\"Code.E0701: Execution failed: Code.E0701: Execution failed: Code.E0401: Keyword execution failed: Code.E0401: Error executing adb command ['adb', '-s', 'RZCT20HFLRM', 'shell', 'pm', 'dump', 'com.samsung.android.calendar']: Command '['adb', '-s', 'RZCT20HFLRM', 'shell', 'pm', 'dump', 'com.samsung.android.calendar']' returned non-zero exit status 1.. Received output = .\")"
    }
    ```

    Maybe adb cannot reach the device

get_driver_session_id
- works

get_interactive_elements
- works when passing without any filter.
- doesn't work when passing a filter. Tried with:
    ```
    {
        "mode": "keyword",
        "keyword": "Get Interactive Elements",
        "params": [["interactive"]],
        "template_images": {}
    }
    ```

    Got this:
    ```
    {
        "detail": "Execution failed: All fallback attempts failed for keyword 'Get Interactive Elements':\n('buttons',) -> OpticsError('Code.E0701: Execution failed: Code.E0701: Execution failed: Code.E0401: Keyword execution failed: Code.E0202: No interactive elements retrieved using available strategies.')"
    }
    ```
    
get_screen_elements
- works but it returns an image as base64 string in the response. A more efficient alternative would be to return a url to the image instead of the base64 string. The image can then be downloaded from the url. 
- This keyword is not present in the docs at: https://mozarkai.github.io/optics-framework/usage/keyword_usage/ but is present in `optics live` tui.

get_text
- failed. Tried:
    ```
    {
      "mode": "keyword",
      "keyword": "Get Text",
      "params": ["//android.widget.Button"],
      "template_images": {}
    }
    ```

    Got:
    ```
    {
      "detail": "Execution failed: All fallback attempts failed for keyword 'Get Text':\n('//android.widget.Button',) -> OpticsError(\"Code.E0701: Execution failed: Code.E0701: Execution failed: Code.E0401: Keyword execution failed: Message: 'value' attribute is unknown for the element. Only the following attributes are supported: [checkable, checked, {class,className}, clickable, {content-desc,contentDescription}, enabled, focusable, focused, {long-clickable,longClickable}, package, password, {resource-id,resourceId}, scrollable, selection-start, selection-end, selected, {text,name}, hint, extras, bounds, displayed, contentSize, {a11y-important,importantForAccessibility}, {screen-reader-focusable,screenReaderFocusable}, {input-type,inputType}, {drawing-order,drawingOrder}, {showing-hint,showingHintText}, {text-entry-key,textEntryKey}, {multiline,multiLine}, dismissable, {a11y-focused,accessibilityFocused}, heading, {live-region,liveRegion}, {context-clickable,contextClickable}, {max-text-length,maxTextLength}, {content-invalid,contentInvalid}, {error,errorText}, {pane-title,paneTitle}, {tooltip-text,tooltipText}, {text-has-clickable-span,textHasClickableSpan}, actions]\\nStacktrace:\\nio.appium.uiautomator2.common.exceptions.NoSuchAttributeException: 'value' attribute is unknown for the element. Only the following attributes are supported: [checkable, checked, {class,className}, clickable, {content-desc,contentDescription}, enabled, focusable, focused, {long-clickable,longClickable}, package, password, {resource-id,resourceId}, scrollable, selection-start, selection-end, selected, {text,name}, hint, extras, bounds, displayed, contentSize, {a11y-important,importantForAccessibility}, {screen-reader-focusable,screenReaderFocusable}, {input-type,inputType}, {drawing-order,drawingOrder}, {showing-hint,showingHintText}, {text-entry-key,textEntryKey}, {multiline,multiLine}, dismissable, {a11y-focused,accessibilityFocused}, heading, {live-region,liveRegion}, {context-clickable,contextClickable}, {max-text-length,maxTextLength}, {content-invalid,contentInvalid}, {error,errorText}, {pane-title,paneTitle}, {tooltip-text,tooltipText}, {text-has-clickable-span,textHasClickableSpan}, actions]\\n\\tat io.appium.uiautomator2.utils.ElementHelpers.generateNoAttributeException(ElementHelpers.java:102)\\n\\tat io.appium.uiautomator2.model.UiObject2Element.getAttribute(UiObject2Element.java:79)\\n\\tat io.appium.uiautomator2.handler.GetElementAttribute.safeHandle(GetElementAttribute.java:24)\\n\\tat io.appium.uiautomator2.handler.request.SafeRequestHandler.handle(SafeRequestHandler.java:59)\\n\\tat io.appium.uiautomator2.server.AppiumServlet.handleRequest(AppiumServlet.java:259)\\n\\tat io.appium.uiautomator2.server.AppiumServlet.handleHttpRequest(AppiumServlet.java:253)\\n\\tat io.appium.uiautomator2.http.ServerHandler.channelRead(ServerHandler.java:77)\\n\\tat io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:374)\\n\\tat io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:360)\\n\\tat io.netty.channel.AbstractChannelHandlerContext.fireChannelRead(AbstractChannelHandlerContext.java:352)\\n\\tat io.netty.handler.codec.MessageToMessageDecoder.channelRead(MessageToMessageDecoder.java:102)\\n\\tat io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:374)\\n\\tat io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:360)\\n\\tat io.netty.channel.AbstractChannelHandlerContext.fireChannelRead(AbstractChannelHandlerContext.java:352)\\n\\tat io.netty.channel.CombinedChannelDuplexHandler$DelegatingChannelHandlerContext.fireChannelRead(CombinedChannelDuplexHandler.java:438)\\n\\tat io.netty.handler.codec.ByteToMessageDecoder.fireChannelRead(ByteToMessageDecoder.java:328)\\n\\tat io.netty.handler.codec.ByteToMessageDecoder.channelRead(ByteToMessageDecoder.java:302)\\n\\tat io.netty.channel.CombinedChannelDuplexHandler.channelRead(CombinedChannelDuplexHandler.java:253)\\n\\tat io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:374)\\n\\tat io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:360)\\n\\tat io.netty.channel.AbstractChannelHandlerContext.fireChannelRead(AbstractChannelHandlerContext.java:352)\\n\\tat io.netty.handler.timeout.IdleStateHandler.channelRead(IdleStateHandler.java:287)\\n\\tat io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:374)\\n\\tat io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:360)\\n\\tat io.netty.channel.AbstractChannelHandlerContext.fireChannelRead(AbstractChannelHandlerContext.java:352)\\n\\tat io.netty.channel.DefaultChannelPipeline$HeadContext.channelRead(DefaultChannelPipeline.java:1422)\\n\\tat io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:374)\\n\\tat io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:360)\\n\\tat io.netty.channel.DefaultChannelPipeline.fireChannelRead(DefaultChannelPipeline.java:931)\\n\\tat io.netty.channel.nio.AbstractNioByteChannel$NioByteUnsafe.read(AbstractNioByteChannel.java:163)\\n\\tat io.netty.channel.nio.NioEventLoop.processSelectedKey(NioEventLoop.java:700)\\n\\tat io.netty.channel.nio.NioEventLoop.processSelectedKeysOptimized(NioEventLoop.java:635)\\n\\tat io.netty.channel.nio.NioEventLoop.processSelectedKeys(NioEventLoop.java:552)\\n\\tat io.netty.channel.nio.NioEventLoop.run(NioEventLoop.java:514)\\n\\tat io.netty.util.concurrent.SingleThreadEventExecutor$6.run(SingleThreadEventExecutor.java:1044)\\n\\tat io.netty.util.internal.ThreadExecutorMap$2.run(ThreadExecutorMap.java:74)\\n\\tat io.netty.util.concurrent.FastThreadLocalRunnable.run(FastThreadLocalRunnable.java:30)\\n\\tat java.lang.Thread.run(Thread.java:1564)\\n\")"
    }
    ```

    When tried with:
    ```
    {
      "mode": "keyword",
      "keyword": "Get Text",
      "params": ["text=Save offer"],
      "template_images": {}
    }
    ```

    Got this:
    ```
    {
      "execution_id": "894dde1a-20bf-4fb6-af15-9464c6c0a3ed",
      "status": "SUCCESS",
      "data": {
        "result": null
      }
    }
    ```
    


initialise_setup
- is not exposed via `optics serve` as written here: https://mozarkai.github.io/optics-framework/usage/keyword_usage/#flow-control-keywords

invoke_api
- started session by passing data into api_data field but when tried with:
   ```
   {
      "mode": "keyword",
      "keyword": "Invoke API",
      "params": ["jsonplaceholder.get_post"],
      "template_images": {}
    }
   ```

   Got:
   ```
   {
      "detail": "Execution failed: All fallback attempts failed for keyword 'Invoke API':\n('jsonplaceholder.get_post',) -> OpticsError(\"Code.E0701: Execution failed: Code.E0701: Execution failed: Code.E0401: Keyword execution failed: Code.E0601: API collection 'jsonplaceholder' not found.\")"
    }
   ```
   
   Had created session with:
   ```
   "api_data": {
    "jsonplaceholder": {
      "name": "jsonplaceholder",
      "base_url": "https://jsonplaceholder.typicode.com",
      "global_headers": {},
      "apis": {
        "get_post": {
          "name": "get_post",
          "endpoint": "/posts/1",
          "request": {
            "method": "GET",
            "headers": {},
            "body": null
          }
        }
      }
    }
  }
   ```

is_element
-  it is present in `optics live` tui but not in docs at: https://mozarkai.github.io/optics-framework/usage/keyword_usage/
- verifier.py:46 has its function definition but the body is just `pass`. Since there is no implementation there is nothing to test.
 
launch_app
- didn't work

launch_other_app
- works in both cases when app is not running and when app is already running but in background.

press_by_coordinates
- works but test repeat paramater doesn't work. It always presses the coordinates once even if repeat param is set to a value greater than 1. It is because `action_keyword.py:339` doesn't use the `repeat` parameter in the `press_by_coordinates()` function.

press_by_percentage
- works, repeat parameter also works.

press_element
- works when element is present on screen

press_keycode
- works but inconsistently. After leaving the session open at `https://mozarkdemo-app-testing.mozark.ai/motesting/interact/` for sometime, it fails to press keycodes.

read_data
- works

run_loop
- TODO

scroll
- works

scroll_from_element
- works

scroll_until_element_appears
- when passing in an appropriate element along with a suitable timeout, the element is scrolled down to and is detected. But when passing in a short timeout it still gives `"status": "SUCCESS"` in the response. Seems misleading. Should have given an error code instead. Scroll successfully stops when element is detected.

select_dropdown_option
- works
- when passed an option which is not present in the dropdown, it selects an incorrect option instead of throwing an error. Should have thrown an error instead
- correctly throws an error when the dropdown element is not present on screen
- it is present in `optics live` tui but not in docs at: https://mozarkai.github.io/optics-framework/usage/keyword_usage/

sleep
- work

start_appium_session
- Didn't test because as per docs at: https://mozarkai.github.io/optics-framework/usage/keyword_usage/#start-appium-session it is automatically called during setup

swipe
- works, but when tested with a wrong request json like this:
    ```
    {
      "mode": "keyword",
      "keyword": "Swipe",
      "params": ["540", "2000", "540", "500"],
      "template_images": {}
    }
    ```

    instead of 
    ```
    {
      "mode": "keyword",
      "keyword": "Swipe",
      "params": ["540", "1200", "down", "500"],
      "template_images": {}
    }
    ```

    it still says `"status": "SUCCESS"` in the response. Should have been a validation error instead since the values in request json fields were not as expected.

swipe_by_percentage
- when passing 
    ```
    {
      "mode": "keyword",
      "keyword": "Swipe Percentage",
      "params": ["50", "50", "up", "30"],
      "template_images": {}
    }
    ```

    it responds with:

    ```
    {
      "detail": {
        "type": "optics:keyword",
        "code": "Code.E0402",
        "status": 404,
        "message": "Keyword Swipe Percentage not found",
        "details": null,
        "meta": null
      }
    }
    ```

    but this is how it is written at docs here: https://mozarkai.github.io/optics-framework/usage/keyword_usage/#swipe-percentage

    `optics live` reports it to be `swipe_by_percentage` instead of `swipe_percentage`. So the docs are wrong. When tried `Swipe By Percentage` instead of `Swipe Percentage`, it worked. So the docs need to be updated.

- The wrong request json problem like in `swipe` keyword above may also exist

swipe_from_element
- works

swipe_until_element_appears
-  works but even if element never appears on screen, it still gives `"status": "SUCCESS"` in the response. Should have given an error code instead. Swipe successfully stops when element is detected.

validate_element
- works. Returns error if element is not present on screen. Returns `"status": "SUCCESS"` if element is present on screen.

validate_screen
- works. Returns its result as `"result": true` or `"result": false` in the response or `"result": false` in the response.