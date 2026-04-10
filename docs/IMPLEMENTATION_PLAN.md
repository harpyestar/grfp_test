# GRFP UI 自动化测试项目实现计划

> **For agentic workers:** 使用 superpowers:executing-plans 或 superpowers:subagent-driven-development 逐步完成任务。

**目标:** 基于 DESIGN.md，创建完整的 Python + Playwright + pytest-playwright + allure UI 自动化测试项目骨架，实现三角色登录功能。

**架构:** 采用 Page Object Model 模式 + 会话复用策略。通过 conftest.py 管理浏览器生命周期，使用 pytest 参数化实现多角色测试，通过 config.py 统一管理环境配置。

**技术栈:** Python 3.9+, Playwright, pytest, pytest-playwright, python-dotenv, allure-pytest

---

## 文件结构规划

```
d:\work_dev\GRFP\grfp-ui-test/
├── requirements.txt                  # 依赖清单
├── pytest.ini                        # pytest 配置
├── .env.test.example                 # 环境变量模板
├── conftest.py                       # 根级浏览器管理
├── DESIGN.md                         # 设计文档
├── IMPLEMENTATION_PLAN.md            # 本计划
│
├── data/
│   ├── __init__.py
│   ├── test_accounts.json            # 账号数据
│   └── fixtures/
│       ├── __init__.py
│       └── accounts.py               # 账号 fixture
│
├── pages/
│   ├── __init__.py
│   ├── common/
│   │   ├── __init__.py
│   │   ├── base_page.py              # POM 基类
│   │   └── login_page.py             # 登录页
│   ├── operate/
│   │   └── __init__.py
│   ├── hotel/
│   │   └── __init__.py
│   └── hotel_group/
│       └── __init__.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                   # 测试级配置
│   ├── auth/
│   │   ├── __init__.py
│   │   └── test_login.py             # 登录测试
│   ├── operate/
│   │   └── __init__.py
│   ├── hotel/
│   │   └── __init__.py
│   ├── hotel_group/
│   │   └── __init__.py
│   └── e2e/
│       └── __init__.py
│
└── utils/
    ├── __init__.py
    ├── config.py                     # 配置管理
    ├── logger.py                     # 日志工具
    └── wait_helper.py                # 等待工具
```

---

## 任务分解

### Task 1: 创建项目目录结构

**Files:**
- Create: `d:\work_dev\GRFP\grfp-ui-test\` (根目录)
- Create: 所有子目录和 `__init__.py`

- [ ] **Step 1: 创建根目录**

```bash
cd d:\work_dev\GRFP
mkdir grfp-ui-test
cd grfp-ui-test
```

- [ ] **Step 2: 创建目录层级**

```bash
# 创建主要目录
mkdir data data\fixtures pages pages\common pages\operate pages\hotel pages\hotel_group
mkdir tests tests\auth tests\operate tests\hotel tests\hotel_group tests\e2e
mkdir utils

# 创建所有 __init__.py
touch data\__init__.py data\fixtures\__init__.py
touch pages\__init__.py pages\common\__init__.py pages\operate\__init__.py pages\hotel\__init__.py pages\hotel_group\__init__.py
touch tests\__init__.py tests\auth\__init__.py tests\operate\__init__.py tests\hotel\__init__.py tests\hotel_group\__init__.py tests\e2e\__init__.py
touch utils\__init__.py
```

- [ ] **Step 3: 验证目录结构**

```bash
tree /F
```

Expected: 显示完整的目录树

- [ ] **Step 4: Commit**

```bash
git init
git add .
git commit -m "chore: initialize project directory structure"
```

---

### Task 2: 创建 requirements.txt

**Files:**
- Create: `requirements.txt`

- [ ] **Step 1: 编写依赖清单**

```bash
cat > requirements.txt << 'EOF'
# Core Testing Framework
pytest==7.4.3
pytest-playwright==0.4.1
playwright==1.40.0

# Configuration Management
python-dotenv==1.0.0

# Reporting
allure-pytest==2.13.2

# Optional: Parallel execution and retry
pytest-xdist==3.5.0
pytest-rerunfailures==12.0

# Optional: Code quality
black==23.12.0
flake8==6.1.0
EOF
```

- [ ] **Step 2: 验证文件内容**

```bash
cat requirements.txt
```

Expected: 显示依赖列表

- [ ] **Step 3: Commit**

```bash
git add requirements.txt
git commit -m "chore: add project dependencies"
```

---

### Task 3: 创建 pytest.ini

**Files:**
- Create: `pytest.ini`

- [ ] **Step 1: 编写 pytest 配置**

```bash
cat > pytest.ini << 'EOF'
[pytest]
# 项目名称
project = grfp-ui-test

# 测试发现
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*

# 输出选项
addopts = 
    -v
    --strict-markers
    --tb=short
    --capture=no

# 标记定义
markers =
    auth: 认证相关测试
    operate: 运营端测试
    hotel: 酒店端测试
    hotelgroup: 酒店集团端测试
    e2e: 端到端测试
    smoke: 冒烟测试
    regression: 回归测试

# 测试路径
testpaths = tests

# 日志
log_cli = true
log_cli_level = INFO
log_cli_format = %(asctime)s [%(levelname)8s] %(message)s
log_cli_date_format = %Y-%m-%d %H:%M:%S

# Allure 报告
plugins = allure_pytest
EOF
```

- [ ] **Step 2: 验证文件内容**

```bash
cat pytest.ini
```

Expected: 显示配置内容

- [ ] **Step 3: Commit**

```bash
git add pytest.ini
git commit -m "chore: add pytest configuration"
```

---

### Task 4: 创建 .env.test.example

**Files:**
- Create: `.env.test.example`

- [ ] **Step 1: 编写环境变量模板**

```bash
cat > .env.test.example << 'EOF'
# 测试环境配置
# 复制为 .env.test 并填充实际值

# 环境选择: test, pre, prod
TEST_ENV=test

# 基础 URL
BASE_URL=https://grfp-test.fangcang.com/

# 浏览器配置
HEADLESS=false
SLOW_MO=100

# 日志级别: DEBUG, INFO, WARNING, ERROR
LOG_LEVEL=INFO

# Allure 报告输出目录
ALLURE_RESULTS_DIR=reports/allure-results

# 超时配置（毫秒）
TIMEOUT_PAGE_LOAD=15000
TIMEOUT_ELEMENT=10000
TIMEOUT_NAVIGATION=15000
EOF
```

- [ ] **Step 2: 创建 .env.test（实际配置）**

```bash
cat > .env.test << 'EOF'
# 测试环境配置 - 本地测试使用
TEST_ENV=test
BASE_URL=https://grfp-test.fangcang.com/
HEADLESS=false
SLOW_MO=100
LOG_LEVEL=INFO
ALLURE_RESULTS_DIR=reports/allure-results
TIMEOUT_PAGE_LOAD=15000
TIMEOUT_ELEMENT=10000
TIMEOUT_NAVIGATION=15000
EOF
```

- [ ] **Step 3: 创建 .gitignore（防止提交 .env.test）**

```bash
cat > .gitignore << 'EOF'
# Environment variables
.env.test
.env.pre
.env.prod

# Reports
reports/
__pycache__/
*.pyc
.pytest_cache/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF
```

- [ ] **Step 4: Commit**

```bash
git add .env.test.example .gitignore
git commit -m "chore: add environment configuration templates"
```

---

### Task 5: 创建 utils/config.py

**Files:**
- Create: `utils/config.py`

- [ ] **Step 1: 编写配置管理模块**

```bash
cat > utils/config.py << 'EOF'
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
EOF
```

- [ ] **Step 2: 验证文件内容**

```bash
cat utils/config.py
```

Expected: 显示完整的配置模块代码

- [ ] **Step 3: Commit**

```bash
git add utils/config.py
git commit -m "feat: add configuration management module"
```

---

### Task 6: 创建 utils/logger.py

**Files:**
- Create: `utils/logger.py`

- [ ] **Step 1: 编写日志工具模块**

```bash
cat > utils/logger.py << 'EOF'
"""
日志工具模块
提供统一的日志记录接口
"""

import logging
import sys
from typing import Optional


class Logger:
    """日志管理类"""
    
    _loggers = {}
    
    @staticmethod
    def get_logger(name: str, level: str = "INFO") -> logging.Logger:
        """
        获取或创建日志记录器
        
        Args:
            name: 日志记录器名称（通常为模块名）
            level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
        Returns:
            logging.Logger 实例
        """
        if name in Logger._loggers:
            return Logger._loggers[name]
        
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))
        
        # 避免重复添加处理器
        if not logger.handlers:
            # 控制台处理器
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
            
            # 格式化
            formatter = logging.Formatter(
                fmt="%(asctime)s [%(name)s] [%(levelname)s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            console_handler.setFormatter(formatter)
            
            logger.addHandler(console_handler)
        
        Logger._loggers[name] = logger
        return logger


# 便捷函数
def get_logger(name: str, level: str = "INFO") -> logging.Logger:
    """获取日志记录器"""
    return Logger.get_logger(name, level)
EOF
```

- [ ] **Step 2: 验证文件内容**

```bash
cat utils/logger.py
```

Expected: 显示完整的日志模块代码

- [ ] **Step 3: Commit**

```bash
git add utils/logger.py
git commit -m "feat: add logging utility module"
```

---

### Task 7: 创建 utils/wait_helper.py

**Files:**
- Create: `utils/wait_helper.py`

- [ ] **Step 1: 编写等待工具模块**

```bash
cat > utils/wait_helper.py << 'EOF'
"""
等待策略工具模块
提供 Playwright 等待操作的便捷封装
"""

from typing import Optional, Callable
from playwright.async_api import Page, expect
import asyncio


class WaitHelper:
    """等待工具类"""
    
    @staticmethod
    async def wait_for_url(
        page: Page,
        url_pattern: str,
        timeout: int = 15000
    ) -> None:
        """
        等待 URL 包含指定模式
        
        Args:
            page: Playwright Page 对象
            url_pattern: URL 模式（支持通配符 * ）
            timeout: 超时时间（毫秒）
        """
        try:
            await page.wait_for_url(url_pattern, timeout=timeout)
        except Exception as e:
            raise TimeoutError(f"URL '{url_pattern}' not found within {timeout}ms: {str(e)}")
    
    @staticmethod
    async def wait_for_selector(
        page: Page,
        selector: str,
        timeout: int = 10000
    ) -> None:
        """
        等待元素出现
        
        Args:
            page: Playwright Page 对象
            selector: CSS 选择器
            timeout: 超时时间（毫秒）
        """
        try:
            await page.wait_for_selector(selector, timeout=timeout)
        except Exception as e:
            raise TimeoutError(f"Selector '{selector}' not found within {timeout}ms: {str(e)}")
    
    @staticmethod
    async def wait_for_load_state(
        page: Page,
        state: str = "networkidle",
        timeout: int = 15000
    ) -> None:
        """
        等待页面加载完成
        
        Args:
            page: Playwright Page 对象
            state: 加载状态 (load, domcontentloaded, networkidle)
            timeout: 超时时间（毫秒）
        """
        try:
            await page.wait_for_load_state(state, timeout=timeout)
        except Exception as e:
            raise TimeoutError(f"Page load state '{state}' not reached within {timeout}ms: {str(e)}")
    
    @staticmethod
    async def wait_for_text(
        page: Page,
        text: str,
        timeout: int = 10000
    ) -> None:
        """
        等待页面包含指定文本
        
        Args:
            page: Playwright Page 对象
            text: 要查找的文本
            timeout: 超时时间（毫秒）
        """
        try:
            await page.locator(f":has-text('{text}')").first.wait_for(timeout=timeout)
        except Exception as e:
            raise TimeoutError(f"Text '{text}' not found within {timeout}ms: {str(e)}")
    
    @staticmethod
    async def sleep(seconds: int) -> None:
        """
        异步睡眠（用于特殊等待场景）
        
        Args:
            seconds: 睡眠秒数
        """
        await asyncio.sleep(seconds)
EOF
```

- [ ] **Step 2: 验证文件内容**

```bash
cat utils/wait_helper.py
```

Expected: 显示完整的等待工具代码

- [ ] **Step 3: Commit**

```bash
git add utils/wait_helper.py
git commit -m "feat: add wait helper utility module"
```

---

### Task 8: 创建 data/test_accounts.json

**Files:**
- Create: `data/test_accounts.json`

- [ ] **Step 1: 编写账号数据文件**

```bash
cat > data/test_accounts.json << 'EOF'
{
  "operate": {
    "email": "yaohui.zheng@fangcang.com",
    "password": "666666",
    "role_name": "Operate"
  },
  "hotel": {
    "email": "hzxgll@qq.com",
    "password": "666666",
    "role_name": "Hotel"
  },
  "hotelgroup": {
    "email": "jiudianjt@qq.com",
    "password": "666666",
    "role_name": "HotelGroup"
  }
}
EOF
```

- [ ] **Step 2: 验证文件内容**

```bash
cat data/test_accounts.json
```

Expected: 显示 JSON 格式的账号数据

- [ ] **Step 3: Commit**

```bash
git add data/test_accounts.json
git commit -m "test: add test account credentials"
```

---

### Task 9: 创建 pages/common/base_page.py

**Files:**
- Create: `pages/common/base_page.py`

- [ ] **Step 1: 编写 POM 基类**

```bash
cat > pages/common/base_page.py << 'EOF'
"""
Page Object Model 基类
封装所有页面通用的交互操作
"""

from playwright.async_api import Page, expect
from utils.logger import get_logger
from utils.wait_helper import WaitHelper
from utils.config import config
from typing import Optional, Any


class BasePage:
    """Page Object Model 基类"""
    
    def __init__(self, page: Page):
        """
        初始化页面对象
        
        Args:
            page: Playwright Page 实例
        """
        self.page = page
        self.logger = get_logger(self.__class__.__name__, config.log_level)
        self.wait_helper = WaitHelper()
    
    async def goto(self, url: str) -> None:
        """
        导航到指定 URL
        
        Args:
            url: 目标 URL
        """
        self.logger.info(f"Navigating to {url}")
        await self.page.goto(url, wait_until="networkidle")
        await self.wait_helper.wait_for_load_state(
            self.page,
            state="networkidle",
            timeout=config.timeout_page_load
        )
    
    async def find_element(self, selector: str) -> Any:
        """
        查找元素
        
        Args:
            selector: CSS 选择器
        
        Returns:
            定位器对象
        """
        self.logger.debug(f"Finding element: {selector}")
        await self.wait_helper.wait_for_selector(
            self.page,
            selector,
            timeout=config.timeout_element
        )
        return self.page.locator(selector)
    
    async def fill(self, selector: str, value: str) -> None:
        """
        填充输入框
        
        Args:
            selector: CSS 选择器
            value: 要填充的值
        """
        self.logger.info(f"Filling {selector} with {value}")
        locator = await self.find_element(selector)
        await locator.fill(value)
    
    async def click(self, selector: str) -> None:
        """
        点击元素
        
        Args:
            selector: CSS 选择器
        """
        self.logger.info(f"Clicking {selector}")
        locator = await self.find_element(selector)
        await locator.click()
    
    async def get_text(self, selector: str) -> str:
        """
        获取元素文本
        
        Args:
            selector: CSS 选择器
        
        Returns:
            元素文本内容
        """
        self.logger.debug(f"Getting text from {selector}")
        locator = await self.find_element(selector)
        return await locator.text_content() or ""
    
    async def get_attribute(self, selector: str, attribute: str) -> Optional[str]:
        """
        获取元素属性
        
        Args:
            selector: CSS 选择器
            attribute: 属性名
        
        Returns:
            属性值
        """
        self.logger.debug(f"Getting attribute '{attribute}' from {selector}")
        locator = await self.find_element(selector)
        return await locator.get_attribute(attribute)
    
    async def is_visible(self, selector: str) -> bool:
        """
        检查元素是否可见
        
        Args:
            selector: CSS 选择器
        
        Returns:
            True 如果可见，False 否则
        """
        try:
            locator = self.page.locator(selector)
            is_visible = await locator.is_visible()
            self.logger.debug(f"Element {selector} visible: {is_visible}")
            return is_visible
        except Exception as e:
            self.logger.warning(f"Element {selector} not found: {str(e)}")
            return False
    
    async def get_current_url(self) -> str:
        """获取当前页面 URL"""
        url = self.page.url
        self.logger.debug(f"Current URL: {url}")
        return url
    
    async def get_page_title(self) -> str:
        """获取页面标题"""
        title = await self.page.title()
        self.logger.debug(f"Page title: {title}")
        return title
    
    async def screenshot(self, path: str) -> None:
        """
        保存页面截图
        
        Args:
            path: 保存路径
        """
        self.logger.info(f"Taking screenshot: {path}")
        await self.page.screenshot(path=path, full_page=True)
EOF
```

- [ ] **Step 2: 验证文件内容**

```bash
cat pages/common/base_page.py
```

Expected: 显示完整的基类代码

- [ ] **Step 3: Commit**

```bash
git add pages/common/base_page.py
git commit -m "feat: add Page Object Model base class"
```

---

### Task 10: 创建 pages/common/login_page.py

**Files:**
- Create: `pages/common/login_page.py`

- [ ] **Step 1: 编写登录页 POM**

```bash
cat > pages/common/login_page.py << 'EOF'
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
    
    # 选择器定义
    EMAIL_INPUT = 'input[type="text"], input[type="email"]'
    PASSWORD_INPUT = 'input[type="password"]'
    LOGIN_BUTTON = 'button[type="submit"], button:has-text("Login")'
    LOGIN_FORM = 'form'
    
    def __init__(self, page: Page):
        """
        初始化登录页
        
        Args:
            page: Playwright Page 实例
        """
        super().__init__(page)
    
    async def navigate_to_login(self) -> None:
        """导航到登录页"""
        self.logger.info("Navigating to login page")
        await self.goto(config.base_url)
        
        # 等待登录表单出现
        await self.wait_helper.wait_for_selector(
            self.page,
            self.LOGIN_FORM,
            timeout=config.timeout_page_load
        )
    
    async def login(self, email: str, password: str) -> Dict[str, Any]:
        """
        执行登录流程
        
        Args:
            email: 邮箱地址
            password: 密码
        
        Returns:
            登录结果 {success: bool, url: str, message: str}
        """
        try:
            self.logger.info(f"Logging in with email: {email}")
            
            # 1. 访问登录页
            await self.navigate_to_login()
            
            # 2. 填充邮箱
            self.logger.debug("Filling email field")
            await self.fill(self.EMAIL_INPUT, email)
            
            # 3. 填充密码
            self.logger.debug("Filling password field")
            await self.fill(self.PASSWORD_INPUT, password)
            
            # 4. 点击登录按钮
            self.logger.info("Clicking login button")
            await self.click(self.LOGIN_BUTTON)
            
            # 5. 等待登录完成（URL 变化到 /home）
            self.logger.debug("Waiting for login to complete")
            await self.wait_helper.wait_for_url(
                self.page,
                "**/home",
                timeout=config.timeout_navigation
            )
            
            # 6. 等待页面加载完成
            await self.wait_helper.wait_for_load_state(
                self.page,
                state="networkidle",
                timeout=config.timeout_page_load
            )
            
            # 获取登录后的 URL
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
        """检查是否在登录页"""
        is_visible = await self.is_visible(self.LOGIN_FORM)
        self.logger.debug(f"Is login page: {is_visible}")
        return is_visible
EOF
```

- [ ] **Step 2: 验证文件内容**

```bash
cat pages/common/login_page.py
```

Expected: 显示完整的登录页代码

- [ ] **Step 3: Commit**

```bash
git add pages/common/login_page.py
git commit -m "feat: add login page object"
```

---

### Task 11: 创建根级 conftest.py

**Files:**
- Create: `conftest.py`

- [ ] **Step 1: 编写浏览器管理配置**

```bash
cat > conftest.py << 'EOF'
"""
根级 pytest 配置文件
管理浏览器实例生命周期和会话复用
"""

import pytest
import asyncio
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from utils.config import config
from utils.logger import get_logger

logger = get_logger("conftest", config.log_level)


# 事件循环 fixture（支持异步测试）
@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# 浏览器实例 fixture（会话级复用）
@pytest.fixture(scope="session")
async def browser() -> Browser:
    """
    创建浏览器实例（会话级，所有测试共享）
    
    Yields:
        Playwright Browser 实例
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


# 浏览器上下文 fixture（函数级，每个测试创建新上下文）
@pytest.fixture
async def browser_context(browser: Browser) -> BrowserContext:
    """
    创建浏览器上下文（函数级）
    
    Args:
        browser: 浏览器实例
    
    Yields:
        Playwright BrowserContext 实例
    """
    logger.info("Creating new browser context")
    context = await browser.new_context()
    yield context
    logger.info("Closing browser context")
    await context.close()


# 页面实例 fixture（函数级）
@pytest.fixture
async def page(browser_context: BrowserContext) -> Page:
    """
    创建页面实例（函数级）
    
    Args:
        browser_context: 浏览器上下文
    
    Yields:
        Playwright Page 实例
    """
    logger.info("Creating new page")
    page = await browser_context.new_page()
    yield page
    logger.info("Closing page")
    await page.close()


# Pytest 钩子
def pytest_configure(config):
    """pytest 启动时调用"""
    logger.info("=" * 80)
    logger.info("GRFP UI Test Suite Started")
    logger.info(f"Environment: {config.test_env}")
    logger.info(f"Base URL: {config.base_url}")
    logger.info("=" * 80)


def pytest_sessionfinish(session, exitstatus):
    """pytest 会话结束时调用"""
    logger.info("=" * 80)
    logger.info("GRFP UI Test Suite Finished")
    logger.info(f"Exit Status: {exitstatus}")
    logger.info("=" * 80)
EOF
```

- [ ] **Step 2: 验证文件内容**

```bash
cat conftest.py
```

Expected: 显示完整的 conftest 代码

- [ ] **Step 3: Commit**

```bash
git add conftest.py
git commit -m "feat: add root conftest with browser management"
```

---

### Task 12: 创建 tests/conftest.py

**Files:**
- Create: `tests/conftest.py`

- [ ] **Step 1: 编写测试级配置**

```bash
cat > tests/conftest.py << 'EOF'
"""
测试级 pytest 配置文件
处理测试参数、登录 fixture 等
"""

import pytest
from playwright.async_api import Page
from pages.common.login_page import LoginPage
from utils.config import config
from utils.logger import get_logger

logger = get_logger("tests.conftest", config.log_level)


# 账号类型参数化
def pytest_generate_tests(metafunc):
    """
    自动参数化测试
    如果测试函数有 account_type 参数，自动生成三个测试用例
    """
    if "account_type" in metafunc.fixturenames:
        account_types = ["operate", "hotel", "hotelgroup"]
        metafunc.parametrize("account_type", account_types)


# 登录页 fixture
@pytest.fixture
async def login_page(page: Page) -> LoginPage:
    """
    创建登录页对象
    
    Args:
        page: Playwright Page 实例
    
    Yields:
        LoginPage 实例
    """
    logger.info("Creating LoginPage object")
    return LoginPage(page)


# 获取账号信息 fixture
@pytest.fixture
def account_info(account_type: str) -> dict:
    """
    获取指定角色的账号信息
    
    Args:
        account_type: 账号类型 (operate, hotel, hotelgroup)
    
    Returns:
        账号信息字典
    """
    logger.info(f"Loading account info for: {account_type}")
    try:
        account = config.get_account(account_type)
        logger.info(f"Account loaded - Type: {account_type}, Email: {account['email']}")
        return account
    except KeyError as e:
        logger.error(f"Account not found: {account_type}")
        raise
EOF
```

- [ ] **Step 2: 验证文件内容**

```bash
cat tests/conftest.py
```

Expected: 显示完整的测试级 conftest 代码

- [ ] **Step 3: Commit**

```bash
git add tests/conftest.py
git commit -m "feat: add tests conftest with parametrization"
```

---

### Task 13: 创建 tests/auth/test_login.py

**Files:**
- Create: `tests/auth/test_login.py`

- [ ] **Step 1: 编写登录测试**

```bash
cat > tests/auth/test_login.py << 'EOF'
"""
登录功能测试
验证各角色能否成功登录系统
"""

import pytest
from playwright.async_api import Page
from pages.common.login_page import LoginPage
from utils.logger import get_logger
from utils.config import config


logger = get_logger("tests.auth.test_login", config.log_level)


@pytest.mark.auth
@pytest.mark.smoke
class TestLogin:
    """登录测试类"""
    
    async def test_login_success(
        self,
        login_page: LoginPage,
        account_info: dict,
        account_type: str
    ):
        """
        测试：成功登录系统
        
        验证点：
        1. 登录后 URL 包含 /home
        2. 页面加载完成
        3. 登录返回成功状态
        
        Args:
            login_page: 登录页对象
            account_info: 账号信息
            account_type: 账号类型 (operate, hotel, hotelgroup)
        """
        logger.info(f"Starting login test for account type: {account_type}")
        
        # 1. 执行登录
        result = await login_page.login(
            email=account_info["email"],
            password=account_info["password"]
        )
        
        # 2. 验证登录成功
        assert result["success"] is True, f"Login failed: {result['message']}"
        logger.info(f"Login successful for {account_type}")
        
        # 3. 验证 URL 包含 /home
        assert "/home" in result["url"], f"Expected /home in URL, got {result['url']}"
        logger.info(f"URL verification passed: {result['url']}")
        
        # 4. 验证页面标题不为空
        page_title = await login_page.get_page_title()
        assert page_title, "Page title is empty"
        logger.info(f"Page title: {page_title}")
        
        # 5. 验证页面可见性
        assert await login_page.page.is_visible("body"), "Page body not visible"
        logger.info(f"✓ Test passed for {account_type} ({account_info['role_name']})")
    
    async def test_login_url_navigation(
        self,
        login_page: LoginPage,
        account_info: dict,
        account_type: str
    ):
        """
        测试：登录后 URL 正确导航到 /home
        
        验证点：
        1. 登录前 URL 应该是 /login 或基础 URL
        2. 登录后 URL 应该包含 /home
        
        Args:
            login_page: 登录页对象
            account_info: 账号信息
            account_type: 账号类型
        """
        logger.info(f"Testing URL navigation for {account_type}")
        
        # 导航到登录页
        await login_page.navigate_to_login()
        login_url = await login_page.get_current_url()
        logger.info(f"Login page URL: {login_url}")
        
        # 执行登录
        result = await login_page.login(
            email=account_info["email"],
            password=account_info["password"]
        )
        
        assert result["success"] is True, f"Login failed: {result['message']}"
        
        # 验证 URL 包含 /home
        current_url = result["url"]
        assert "/home" in current_url, f"Expected /home in URL, got {current_url}"
        assert current_url != login_url, "URL should change after login"
        
        logger.info(f"✓ URL navigation test passed for {account_type}")
    
    async def test_login_page_title(
        self,
        login_page: LoginPage,
        account_info: dict,
        account_type: str
    ):
        """
        测试：登录后页面标题正确
        
        验证点：
        1. 页面标题不为空
        2. 页面标题不包含 "error" 或异常信息
        
        Args:
            login_page: 登录页对象
            account_info: 账号信息
            account_type: 账号类型
        """
        logger.info(f"Testing page title for {account_type}")
        
        # 执行登录
        result = await login_page.login(
            email=account_info["email"],
            password=account_info["password"]
        )
        
        assert result["success"] is True
        
        # 获取页面标题
        page_title = await login_page.get_page_title()
        logger.info(f"Page title after login: {page_title}")
        
        # 验证页面标题
        assert page_title, "Page title should not be empty"
        assert "error" not in page_title.lower(), f"Title contains error: {page_title}"
        
        logger.info(f"✓ Page title test passed for {account_type}")
EOF
```

- [ ] **Step 2: 验证文件内容**

```bash
cat tests/auth/test_login.py
```

Expected: 显示完整的测试代码

- [ ] **Step 3: Commit**

```bash
git add tests/auth/test_login.py
git commit -m "test: add parametrized login tests for three roles"
```

---

### Task 14: 创建 data/fixtures/accounts.py

**Files:**
- Create: `data/fixtures/accounts.py`

- [ ] **Step 1: 编写账号 fixture 模块**

```bash
cat > data/fixtures/accounts.py << 'EOF'
"""
账号相关的 pytest fixture
"""

import pytest
from utils.config import config


@pytest.fixture
def operate_account():
    """获取运营端账号"""
    return config.get_account("operate")


@pytest.fixture
def hotel_account():
    """获取酒店端账号"""
    return config.get_account("hotel")


@pytest.fixture
def hotelgroup_account():
    """获取酒店集团端账号"""
    return config.get_account("hotelgroup")


@pytest.fixture(params=["operate", "hotel", "hotelgroup"])
def any_account(request):
    """获取任意角色的账号（参数化）"""
    return config.get_account(request.param)
EOF
```

- [ ] **Step 2: 验证文件内容**

```bash
cat data/fixtures/accounts.py
```

Expected: 显示完整的 fixture 代码

- [ ] **Step 3: Commit**

```bash
git add data/fixtures/accounts.py
git commit -m "test: add account fixtures"
```

---

### Task 15: 创建 reports 目录

**Files:**
- Create: `reports/` 目录结构

- [ ] **Step 1: 创建 reports 目录**

```bash
mkdir -p reports/allure-results
```

- [ ] **Step 2: 创建 .gitkeep 保留目录**

```bash
touch reports/.gitkeep
touch reports/allure-results/.gitkeep
```

- [ ] **Step 3: 验证目录创建**

```bash
ls -la reports/
```

Expected: 显示 reports 目录结构

- [ ] **Step 4: Commit**

```bash
git add reports/.gitkeep reports/allure-results/.gitkeep
git commit -m "chore: add reports directory structure"
```

---

### Task 16: 安装依赖并运行测试

**Files:**
- No new files, just verification

- [ ] **Step 1: 安装 Python 依赖**

```bash
pip install -r requirements.txt
```

Expected: 成功安装所有依赖，最后显示 "Successfully installed ..."

- [ ] **Step 2: 验证 Playwright 安装**

```bash
python -m playwright install chromium
```

Expected: Chromium 浏览器下载完成

- [ ] **Step 3: 验证项目结构完整性**

```bash
python -c "from utils.config import config; print(f'✓ Config loaded - ENV: {config.test_env}, URL: {config.base_url}')"
```

Expected: 输出 "✓ Config loaded - ENV: test, URL: https://grfp-test.fangcang.com/"

- [ ] **Step 4: 列出所有测试用例**

```bash
pytest --collect-only tests/auth/test_login.py
```

Expected: 显示发现的 9 个测试用例（3 个测试方法 × 3 个参数化账号）

- [ ] **Step 5: 运行登录测试（无头模式）**

```bash
HEADLESS=true SLOW_MO=50 pytest tests/auth/test_login.py -v --tb=short
```

Expected: 所有 9 个测试通过（PASSED）

- [ ] **Step 6: 生成 Allure 报告**

```bash
pytest tests/auth/test_login.py -v --alluredir=reports/allure-results
```

Expected: 测试通过，报告生成到 reports/allure-results

- [ ] **Step 7: Commit**

```bash
git add .
git commit -m "test: verify all login tests pass"
```

---

### Task 17: 最终验证和文档

**Files:**
- Create: `README.md`

- [ ] **Step 1: 编写 README**

```bash
cat > README.md << 'EOF'
# GRFP UI 自动化测试项目

Python + Playwright + pytest 自动化测试框架

## 快速开始

### 环境需求
- Python 3.9+
- pip

### 安装

```bash
# 安装依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
python -m playwright install chromium
```

### 配置

复制环境变量模板并修改：
```bash
cp .env.test.example .env.test
```

编辑 `.env.test`，设置正确的 BASE_URL 和其他参数。

### 运行测试

#### 运行所有登录测试
```bash
pytest tests/auth/test_login.py -v
```

#### 运行特定角色的测试
```bash
pytest tests/auth/test_login.py::TestLogin::test_login_success[operate] -v
```

#### 生成 Allure 报告
```bash
pytest tests/auth/test_login.py --alluredir=reports/allure-results
allure serve reports/allure-results
```

#### 无头模式运行（用于 CI/CD）
```bash
HEADLESS=true pytest tests/auth/test_login.py -v
```

## 项目结构

```
grfp-ui-test/
├── conftest.py                # 根级配置（浏览器管理）
├── pytest.ini                 # pytest 配置
├── requirements.txt           # 依赖清单
├── .env.test.example          # 环境变量模板
│
├── pages/
│   └── common/
│       ├── base_page.py       # POM 基类
│       └── login_page.py      # 登录页对象
│
├── tests/
│   ├── conftest.py            # 测试级配置
│   └── auth/
│       └── test_login.py      # 登录测试
│
├── data/
│   └── test_accounts.json     # 测试账号
│
└── utils/
    ├── config.py              # 配置管理
    ├── logger.py              # 日志工具
    └── wait_helper.py         # 等待工具
```

## 关键特性

- ✅ Page Object Model 设计模式
- ✅ 会话复用（减少重复登录）
- ✅ 参数化多角色测试
- ✅ 环境灵活切换 (test/pre/prod)
- ✅ Allure 报告集成
- ✅ 详细日志输出

## 后续扩展

- 权限和菜单可见性测试
- 功能模块测试
- E2E 业务流程测试
- 性能和安全测试

## 文档

- [DESIGN.md](DESIGN.md) - 项目设计文档
- [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) - 实现计划
EOF
```

- [ ] **Step 2: 验证 README 内容**

```bash
cat README.md
```

Expected: 显示完整的 README 内容

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: add project README"
```

---

### Task 18: 最终项目验证

**Files:**
- No new files

- [ ] **Step 1: 显示完整的项目结构**

```bash
tree /F
```

Expected: 显示所有已创建的文件和目录

- [ ] **Step 2: 验证所有必要文件存在**

```bash
echo "Checking essential files..."
for file in conftest.py pytest.ini requirements.txt .env.test DESIGN.md README.md; do
  if [ -f "$file" ]; then
    echo "✓ $file"
  else
    echo "✗ $file MISSING"
  fi
done
```

Expected: 所有文件都显示 ✓

- [ ] **Step 3: 运行完整测试套件（验收测试）**

```bash
pytest tests/auth/test_login.py -v --tb=short --alluredir=reports/allure-results
```

Expected: 
- 9 个测试全部通过 (3 个测试方法 × 3 个参数化账号)
- 所有断言验证成功

- [ ] **Step 4: 生成最终统计**

```bash
pytest tests/ --collect-only -q
```

Expected: 显示发现的所有测试用例总数

- [ ] **Step 5: 最终 Commit**

```bash
git log --oneline | head -10
```

Expected: 显示所有提交记录

- [ ] **Step 6: 创建最终标签**

```bash
git tag -a v1.0.0 -m "Initial GRFP UI test project with login implementation"
```

---

## 验收标准

✅ **通过以下所有条件后，项目骨架完成：**

1. ✅ 目录结构完整（所有目录和 __init__.py 已创建）
2. ✅ 核心配置文件完成（requirements.txt, pytest.ini, .env 模板）
3. ✅ 工具库实现（config.py, logger.py, wait_helper.py）
4. ✅ POM 基类和登录页完成（base_page.py, login_page.py）
5. ✅ 浏览器管理 fixture 完成（conftest.py）
6. ✅ 三角色参数化登录测试完成并全部通过
7. ✅ Allure 报告可生成
8. ✅ 所有代码已提交，有明确的提交信息

---

## 下一步（不在本计划范围内）

- [ ] 权限和菜单可见性验证测试
- [ ] 项目管理功能测试（创建、编辑、发布）
- [ ] 报价管理功能测试
- [ ] 多角色 E2E 流程测试
- [ ] CI/CD 流水线集成
- [ ] 性能测试和安全测试

EOF
```

Expected: 完整的计划文档

- [ ] **Step 7: 最终 Commit**

```bash
git add IMPLEMENTATION_PLAN.md
git commit -m "docs: add implementation plan for reference"
```

---

## 计划完成

✅ **共 18 个任务，涵盖：**
- 项目初始化（Task 1）
- 配置文件创建（Task 2-4）
- 工具库实现（Task 5-7）
- 测试数据准备（Task 8）
- Page Object Model 实现（Task 9-10）
- 浏览器和测试配置（Task 11-12）
- 测试实现（Task 13-14）
- 项目验证和文档（Task 15-18）

✅ **最终产物：**
- 完整的项目骨架
- 功能完整的登录测试（三角色参数化）
- 所有核心工具库和配置
- 完整的文档和提交记录
- 可直接运行的测试套件

