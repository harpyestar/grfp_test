"""
E2E 测试 conftest.py
提供双 context 管理：Operate 和 Hotel 各自独立的浏览器上下文
使用同 browser + 两个 context 模式，存储完全隔离（cookies/localStorage 互不影响）
"""

import pytest
from pages.common.login_page import LoginPage
from utils.config import config
from utils.logger import get_logger

logger = get_logger("tests.e2e.conftest", config.log_level)


# ======================================================================
# Operate 端 fixtures（Module 级，整个模块共享登录状态）
# ======================================================================

@pytest.fixture(scope="module")
def operate_e2e_context(browser, event_loop):
    """Operate 端 browser context（Module 级）"""
    logger.info("Creating operate E2E browser context [SCOPE: module]")

    async def _create():
        return await browser.new_context(viewport=config.viewport)

    context = event_loop.run_until_complete(_create())
    yield context

    async def _close():
        logger.info("Closing operate E2E browser context")
        await context.close()

    event_loop.run_until_complete(_close())


@pytest.fixture(scope="module")
def operate_e2e_page(operate_e2e_context, event_loop):
    """Operate 端页面（Module 级）"""
    logger.info("Creating operate E2E page [SCOPE: module]")

    async def _create():
        return await operate_e2e_context.new_page()

    page = event_loop.run_until_complete(_create())
    yield page

    async def _close():
        logger.info("Closing operate E2E page")
        await page.close()

    event_loop.run_until_complete(_close())


@pytest.fixture(scope="module")
def operate_e2e_login(operate_e2e_page, event_loop):
    """Operate 端登录（Module 级，整个模块只登录一次）"""
    logger.info("Setting up operate E2E login [SCOPE: module]")

    account = config.get_account("operate")
    logger.info(f"Loading operate account: {account['email']}")

    async def _login():
        login_page = LoginPage(operate_e2e_page)
        result = await login_page.login(account["email"], account["password"])
        if not result["success"]:
            raise Exception(
                f"Operate E2E login failed: {result['message']}"
            )
        logger.info(f"Operate E2E login successful (ONE-TIME for module)")

    event_loop.run_until_complete(_login())
    yield operate_e2e_page


# ======================================================================
# Hotel 端 fixtures（Module 级，独立 context）
# ======================================================================

@pytest.fixture(scope="module")
def hotel_e2e_context(browser, event_loop):
    """Hotel 端 browser context（Module 级，与 operate 隔离）"""
    logger.info("Creating hotel E2E browser context [SCOPE: module]")

    async def _create():
        return await browser.new_context(viewport=config.viewport)

    context = event_loop.run_until_complete(_create())
    yield context

    async def _close():
        logger.info("Closing hotel E2E browser context")
        await context.close()

    event_loop.run_until_complete(_close())


@pytest.fixture(scope="module")
def hotel_e2e_page(hotel_e2e_context, event_loop):
    """Hotel 端页面（Module 级）"""
    logger.info("Creating hotel E2E page [SCOPE: module]")

    async def _create():
        return await hotel_e2e_context.new_page()

    page = event_loop.run_until_complete(_create())
    yield page

    async def _close():
        logger.info("Closing hotel E2E page")
        await page.close()

    event_loop.run_until_complete(_close())


@pytest.fixture(scope="module")
def hotel_e2e_login(hotel_e2e_page, event_loop):
    """Hotel 端登录（Module 级，整个模块只登录一次）"""
    logger.info("Setting up hotel E2E login [SCOPE: module]")

    account = config.get_account("hotel")
    logger.info(f"Loading hotel account: {account['email']}")

    async def _login():
        login_page = LoginPage(hotel_e2e_page)
        result = await login_page.login(account["email"], account["password"])
        if not result["success"]:
            raise Exception(
                f"Hotel E2E login failed: {result['message']}"
            )
        logger.info(f"Hotel E2E login successful (ONE-TIME for module)")

    event_loop.run_until_complete(_login())
    yield hotel_e2e_page