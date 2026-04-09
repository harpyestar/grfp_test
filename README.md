# GRFP UI 自动化测试项目

Python + Playwright + pytest 自动化测试框架

## 快速开始

### 环境需求
- Python 3.9+
- pip

### 安装

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

### 配置

```bash
cp .env.test.example .env.test
```

### 运行测试

#### 运行所有登录测试
```bash
pytest tests/auth/test_login.py -v
```

#### 无头模式（CI/CD）
```bash
HEADLESS=true pytest tests/auth/test_login.py -v
```

#### 生成 Allure 报告
```bash
pytest tests/auth/test_login.py --alluredir=reports/allure-results
```

## 项目结构

```
grfp-ui-test/
├── conftest.py                # 浏览器管理
├── pytest.ini                 # pytest 配置
├── requirements.txt           # 依赖
├── pages/
│   └── common/
│       ├── base_page.py       # POM 基类
│       └── login_page.py      # 登录页
├── tests/
│   ├── conftest.py            # 参数化配置
│   └── auth/
│       └── test_login.py      # 登录测试
├── data/
│   └── test_accounts.json     # 测试账号
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

## 文档

- [DESIGN.md](DESIGN.md) - 项目设计文档
- [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) - 实现计划
