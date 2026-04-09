"""
根级 conftest.py
全局 fixture 管理：浏览器、浏览器上下文、页面生命周期
"""

import pytest
import asyncio
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from utils.config import config
from utils.logger import get_logger

logger = get_logger("conftest", config.log_level)


@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环（pytest-asyncio）"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def browser() -> Browser:
    """
    浏览器 fixture（会话级）
    启动 Chromium 浏览器，在所有测试结束后关闭
    """
    logger.info("Starting browser")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=config.headless,
            slow_mo=config.slow_mo
        )
        logger.info(f"Browser launched - Headless: {config.headless}, SlowMo: {config.slow_mo}ms")
        yield browser
        logger.info("Closing browser")
        await browser.close()


@pytest.fixture
async def browser_context(browser: Browser) -> BrowserContext:
    """
    浏览器上下文 fixture（测试级）
    每个测试获得独立的浏览器上下文
    """
    logger.info("Creating new browser context")
    context = await browser.new_context()
    yield context
    logger.info("Closing browser context")
    await context.close()


@pytest.fixture
async def page(browser_context: BrowserContext) -> Page:
    """
    页面 fixture（测试级）
    每个测试获得独立的页面
    """
    logger.info("Creating new page")
    page = await browser_context.new_page()
    yield page
    logger.info("Closing page")
    await page.close()


def pytest_configure(config):
    """pytest 启动时执行 - access our config via the global import"""
    from utils.config import config as app_config
    logger.info("=" * 80)
    logger.info("GRFP UI Test Suite Started")
    logger.info(f"Environment: {app_config.test_env}")
    logger.info(f"Base URL: {app_config.base_url}")
    logger.info("=" * 80)


def pytest_sessionfinish(session, exitstatus):
    """pytest 结束时执行"""
    logger.info("=" * 80)
    logger.info("GRFP UI Test Suite Finished")
    logger.info(f"Exit Status: {exitstatus}")
    logger.info("=" * 80)
