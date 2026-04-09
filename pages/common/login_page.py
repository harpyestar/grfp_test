"""
登录页面对象模型
处理登录相关的交互操作
"""

from playwright.async_api import Page
from pages.common.base_page import BasePage
from utils.config import config
from typing import Dict, Any


class LoginPage(BasePage):
    """登录页 Page Object"""

    EMAIL_INPUT = 'input[type="text"], input[type="email"]'
    PASSWORD_INPUT = 'input[type="password"]'
    LOGIN_BUTTON = 'button[type="submit"], button:has-text("Login")'
    LOGIN_FORM = 'form'

    def __init__(self, page: Page):
        super().__init__(page)

    async def navigate_to_login(self) -> None:
        self.logger.info("Navigating to login page")
        await self.goto(config.base_url)

        await self.wait_helper.wait_for_selector(
            self.page,
            self.LOGIN_FORM,
            timeout=config.timeout_page_load
        )

    async def login(self, email: str, password: str) -> Dict[str, Any]:
        try:
            self.logger.info(f"Logging in with email: {email}")

            await self.navigate_to_login()

            self.logger.debug("Filling email field")
            await self.fill(self.EMAIL_INPUT, email)

            self.logger.debug("Filling password field")
            await self.fill(self.PASSWORD_INPUT, password)

            self.logger.info("Clicking login button")
            await self.click(self.LOGIN_BUTTON)

            self.logger.debug("Waiting for login to complete")
            await self.wait_helper.wait_for_url(
                self.page,
                "**/home",
                timeout=config.timeout_navigation
            )

            await self.wait_helper.wait_for_load_state(
                self.page,
                state="networkidle",
                timeout=config.timeout_page_load
            )

            current_url = await self.get_current_url()
            self.logger.info(f"Login successful. Current URL: {current_url}")

            return {
                "success": True,
                "url": current_url,
                "message": "Login successful"
            }

        except Exception as e:
            error_message = f"Login failed: {str(e)}"
            self.logger.error(error_message)
            current_url = await self.get_current_url()

            return {
                "success": False,
                "url": current_url,
                "message": error_message
            }

    async def is_login_page(self) -> bool:
        is_visible = await self.is_visible(self.LOGIN_FORM)
        self.logger.debug(f"Is login page: {is_visible}")
        return is_visible
