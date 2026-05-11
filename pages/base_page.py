from playwright.sync_api import Page
from utils.logger import get_logger
from config.config_reader import SCREENSHOT_DIR

logger = get_logger(__name__)

class BasePage:
    def __init__(self, page:Page):
        self.page = page
        
    def navigate(self, url:str):
        logger.info(f"Navigating to: {url}")
        self.page.goto(url)
    
    def get_title(self) -> str:
        return self.page.title()

    def get_current_url(self) -> str:
        return self.page.url
    
    def wait_for_url(self, url_pattern: str):
        self.page.wait_for_url(url_pattern)
        
    def wait_for_selector(self, selector: str):
        self.page.wait_for_selector(selector)
    
    def take_screenshot(self, name: str):
        path = f"{SCREENSHOT_DIR}/{name}.png"
        self.page.screenshot(path=path)
        logger.info(f"Screenshot saved: {path}")
        
    
        