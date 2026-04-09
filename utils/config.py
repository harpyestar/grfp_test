"""
配置管理模块
负责读取 .env 文件和 test_accounts.json，提供统一的配置接口
"""

import os
import json
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv


class Config:
    """项目配置类"""

    # 项目根目录
    PROJECT_ROOT = Path(__file__).parent.parent

    # 数据目录
    DATA_DIR = PROJECT_ROOT / "data"
    ACCOUNTS_FILE = DATA_DIR / "test_accounts.json"

    def __init__(self, env_file: str = ".env.test"):
        """
        初始化配置

        Args:
            env_file: .env 文件名（不包括路径，自动在项目根目录查找）
        """
        self.env_path = self.PROJECT_ROOT / env_file

        # 加载 .env 文件
        if self.env_path.exists():
            load_dotenv(self.env_path)
        else:
            print(f"Warning: {self.env_path} not found, using system environment variables")

        # 加载 test_accounts.json
        self.accounts = self._load_accounts()

    def _load_accounts(self) -> Dict[str, Dict[str, str]]:
        """加载测试账号数据"""
        if not self.ACCOUNTS_FILE.exists():
            raise FileNotFoundError(f"Accounts file not found: {self.ACCOUNTS_FILE}")

        with open(self.ACCOUNTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    @property
    def base_url(self) -> str:
        """获取基础 URL"""
        return os.getenv("BASE_URL", "https://grfp-test.fangcang.com/")

    @property
    def test_env(self) -> str:
        """获取测试环境: test/pre/prod"""
        return os.getenv("TEST_ENV", "test")

    @property
    def headless(self) -> bool:
        """获取无头模式"""
        return os.getenv("HEADLESS", "false").lower() == "true"

    @property
    def slow_mo(self) -> int:
        """获取动作减速时间（毫秒）"""
        return int(os.getenv("SLOW_MO", "100"))

    @property
    def log_level(self) -> str:
        """获取日志级别"""
        return os.getenv("LOG_LEVEL", "INFO")

    @property
    def timeout_page_load(self) -> int:
        """获取页面加载超时（毫秒）"""
        return int(os.getenv("TIMEOUT_PAGE_LOAD", "15000"))

    @property
    def timeout_element(self) -> int:
        """获取元素查询超时（毫秒）"""
        return int(os.getenv("TIMEOUT_ELEMENT", "10000"))

    @property
    def timeout_navigation(self) -> int:
        """获取导航超时（毫秒）"""
        return int(os.getenv("TIMEOUT_NAVIGATION", "15000"))

    @property
    def allure_results_dir(self) -> str:
        """获取 Allure 报告输出目录"""
        return os.getenv("ALLURE_RESULTS_DIR", "reports/allure-results")

    def get_account(self, account_type: str) -> Dict[str, str]:
        """
        获取指定角色的账号信息

        Args:
            account_type: 账号类型 (operate, hotel, hotelgroup)

        Returns:
            账号信息字典 {email, password, role_name}

        Raises:
            KeyError: 账号类型不存在
        """
        if account_type not in self.accounts:
            raise KeyError(f"Account type '{account_type}' not found in {self.ACCOUNTS_FILE}")

        return self.accounts[account_type]


# 创建全局配置实例
config = Config()
