from playwright.sync_api import Page
from utils.logger import get_logger

logger = get_logger(__name__)


def check_with_timeout(page: Page, selector: str, timeout: int = 1000) -> bool:
    """
    Checks whether a DOM element is visible and contains a purely numeric text value
    within the given timeout (milliseconds).

    Used by AccountsPage to scan table rows without knowing the row count in advance.
    Returns False when a row is missing or non-numeric, signalling the end of the list.

    Returns:
        True  — element is visible and its stripped text content is all digits
        False — element not found, not visible within timeout, or text is not numeric
    """
    try:
        locator = page.locator(selector)
        locator.wait_for(state="visible", timeout=timeout)

        text = locator.text_content()

        # Only count rows whose first column contains an account number (digits only)
        if text and text.strip().isdigit():
            return True

        logger.debug(f"Selector '{selector}' found but text is not numeric: '{text}'")
        return False

    except Exception:
        # Timeout or element not found — treat as end of list, not a hard failure
        logger.debug(f"Selector '{selector}' not found within {timeout}ms — stopping row scan")
        return False