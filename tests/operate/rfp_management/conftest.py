"""
Operate 角色测试的 conftest.py
定义 operate 相关的 fixtures
"""

import pytest
from pages.common.login_page import LoginPage
from utils.config import config
from utils.logger import get_logger

logger = get_logger("tests.operate.rfp_management.conftest", config.log_level)


@pytest.fixture
async def operate_user(page):
    """
    Operate 角色用户登录 fixture
    自动登录 operate 账号并返回登录后的 page 对象

    Args:
        page: Playwright Page 对象

    Returns:
        page: 已登录的 Page 对象
    """
    logger.info("Setting up operate user fixture - performing login")

    try:
        # 获取 operate 账号信息
        account = config.get_account("operate")
        logger.info(f"Loading operate account: {account['email']}")

        # 创建 LoginPage 对象并执行登录
        login_page = LoginPage(page)
        result = await login_page.login(account["email"], account["password"])

        if result["success"]:
            logger.info(f"Operate user login successful - URL: {result['url']}")
            # 登录成功后，返回已登录状态的 page
            yield page
        else:
            error_msg = f"Operate user login failed: {result['message']}"
            logger.error(error_msg)
            raise Exception(error_msg)

    except Exception as e:
        error_msg = f"Failed to set up operate user fixture: {str(e)}"
        logger.error(error_msg)
        raise

    finally:
        logger.info("Cleaning up operate user fixture")
