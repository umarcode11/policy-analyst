import time

def with_fallback(primary_func, fallback_func=None, retries=2, delay=2):
    """
    Tries primary_func. If it fails, retries up to `retries` times.
    If still failing, calls fallback_func if provided.
    Returns result or a graceful error message.
    """
    last_error = None

    for attempt in range(1, retries + 1):
        try:
            print(f"[Attempt {attempt}] Running primary function...")
            result = primary_func()
            if result and len(str(result).strip()) > 10:
                return result
            else:
                raise ValueError("Empty or too-short response received.")
        except Exception as e:
            last_error = e
            print(f"[Attempt {attempt} Failed] {e}")
            time.sleep(delay)

    if fallback_func:
        try:
            print("[Fallback] Primary failed. Trying fallback function...")
            return fallback_func()
        except Exception as e:
            print(f"[Fallback Failed] {e}")

    return (
        "Unable to complete the request at this time. "
        "The primary tool and fallback both failed. "
        f"Last error: {last_error}"
    )


def validate_output(output: str, min_length: int = 50) -> bool:
    """
    Validates that an output is non-empty and meets minimum length.
    """
    if not output or not isinstance(output, str):
        return False
    if len(output.strip()) < min_length:
        return False
    return True


def safe_tool_call(tool_func, fallback_message="Tool unavailable. Using cached/default data.", *args, **kwargs):
    """
    Wraps a tool call safely. Returns fallback message if tool crashes.
    """
    try:
        result = tool_func(*args, **kwargs)
        return result
    except Exception as e:
        print(f"[Tool Failure] {e}")
        return fallback_message
    