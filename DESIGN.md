# GRFP UI 自动化测试项目 - 设计文档

**日期**: 2026-04-09  
**版本**: 1.0  
**状态**: 已批准

---

## 1. 项目概述

### 1.1 目标
基于 CLAUDE.md 中已验证的 GRFP 系统架构，创建 Python + Playwright 自动化测试项目的骨架。首阶段实现登录功能（支持三个角色：Operate、Hotel、HotelGroup），为后续的功能测试奠定基础。

### 1.2 成功标准
- ✅ 项目结构完整，可支持三个角色的登录参数化测试
- ✅ 登录流程可复用会话，支持后续测试快速执行
- ✅ POM 模式实现，易于扩展新的页面对象
- ✅ 环境配置灵活（test/pre/prod），支持不同环境切换
- ✅ 测试可执行，三个角色的登录验证通过

---

## 2. 项目结构设计

### 2.1 物理目录结构

```
d:\work_dev\GRFP\grfp-ui-test/
├── requirements.txt                  # 项目依赖清单
├── pytest.ini                        # pytest 全局配置
├── DESIGN.md                         # 本设计文档
│
├── .env.test.example                 # 环境变量示例（提交 git）
├── .env.test                         # 实际配置（.gitignore，不提交）
├── .env.pre.example                  # 预发布环境示例
├── .env.prod.example                 # 生产环境示例
│
├── conftest.py                       # 根级 conftest（浏览器初始化、会话管理）
│
├── data/
│   ├── __init__.py
│   ├── test_accounts.json            # 测试账号数据（三角色）
│   └── fixtures/
│       ├── __init__.py
│       └── accounts.py               # 账号 fixture 函数
│
├── pages/
│   ├── __init__.py
│   ├── common/
│   │   ├── __init__.py
│   │   ├── base_page.py              # Page Object 基类
│   │   └── login_page.py             # 登录页 POM
│   │
│   ├── operate/                      # 占位（后续补充功能页）
│   │   └── __init__.py
│   │
│   ├── hotel/                        # 占位（后续补充功能页）
│   │   └── __init__.py
│   │
│   └── hotel_group/                  # 占位（后续补充功能页）
│       └── __init__.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                   # 测试级 conftest（page fixture）
│   │
│   ├── auth/
│   │   ├── __init__.py
│   │   └── test_login.py             # 登录测试（参数化三角色）
│   │
│   ├── operate/                      # 占位（后续补充运营端测试）
│   │   └── __init__.py
│   │
│   ├── hotel/                        # 占位（后续补充酒店端测试）
│   │   └── __init__.py
│   │
│   ├── hotel_group/                  # 占位（后续补充集团端测试）
│   │   └── __init__.py
│   │
│   └── e2e/                          # 占位（后续补充端到端测试）
│       └── __init__.py
│
└── utils/
    ├── __init__.py
    ├── config.py                     # 配置管理（.env 读取、URL 解析）
    ├── logger.py                     # 日志工具
    └── wait_helper.py                # 等待策略工具
```

### 2.2 目录功能说明

| 目录 | 功能 | 阶段 |
|------|------|------|
| `conftest.py` (根) | 管理浏览器实例、会话复用、初始化 | 本阶段 |
| `data/` | 测试数据（账号、模板等） | 本阶段 |
| `pages/common/` | 基类 + 登录页 POM | 本阶段 |
| `pages/{operate,hotel,hotel_group}/` | 功能页对象模型 | 后续阶段 |
| `tests/auth/` | 身份认证测试（登录、会话） | 本阶段 |
| `tests/{operate,hotel,hotel_group}/` | 角色功能测试 | 后续阶段 |
| `tests/e2e/` | 多角色 E2E 流程测试 | 后续阶段 |
| `utils/` | 工具函数库 | 本阶段 |

---

## 3. 核心设计决策

### 3.1 会话复用策略

**选择**: 会话持久化（Option B）

**原理**:
- 首次登录时，使用 Playwright 的 `browser.context()` 创建持久化上下文
- 登录成功后，浏览器自动保存 cookies
- 后续测试直接使用同一上下文，复用 cookies，无需重复登录

**优势**:
- 测试速度快（避免频繁登录）
- 减少服务端负载
- 支持后续集成测试快速执行

**缺点**:
- 测试间可能存在数据污染风险（需要测试设计时规避）

### 3.2 POM 模式实现

**层级**:
1. **base_page.py** - 基类，封装常用操作
   - `find_element(selector)` - 查找元素
   - `wait_for_element(selector, timeout)` - 等待元素出现
   - `fill(selector, value)` - 填充输入框
   - `click(selector)` - 点击元素
   - `get_text(selector)` - 获取文本
   
2. **login_page.py** - 继承基类，提供登录接口
   - `login(email, password)` - 高级接口，完成登录流程
   - 返回登录结果和当前 URL

3. **后续功能页** - 各功能页继承基类
   - 例：`pages/operate/contracting/contracting_list.py`

### 3.3 参数化多角色测试

**实现方式**: pytest 参数化装饰器

```python
@pytest.mark.parametrize("account_type", ["operate", "hotel", "hotelgroup"])
def test_login_success(browser, account_type):
    # 同一测试函数自动执行三次，每次一个角色
```

**优势**:
- 减少测试代码重复
- 自动生成三个独立的测试用例
- 报告清晰（test_login_success[operate], test_login_success[hotel], ...)

### 3.4 环境管理

**环境定义**:
```
TEST_ENV 支持的值：
  - test     → https://grfp-test.fangcang.com/      (测试环境)
  - pre      → https://grfp-pre.fangcang.com/       (预发布环境)  
  - prod     → https://grfp.fangcang.com/           (生产环境)
```

**配置方式**:
- 使用 `.env.test` / `.env.pre` / `.env.prod` 管理不同环境配置
- `utils/config.py` 统一读取，优先级：命令行参数 > 环境变量 > .env 文件

### 3.5 数据管理

**test_accounts.json 结构**:
```json
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
```

---

## 4. 登录流程实现

### 4.1 测试执行流程

```
test_login.py::test_login_success[operate]
    ↓
1. fixture 初始化浏览器 (Playwright chromium)
2. 加载 test_accounts.json，获取 operate 账号
3. 创建 LoginPage 实例
4. 调用 login_page.login(email, pwd)
    └─ 访问 BASE_URL
    └─ 填充邮箱、密码
    └─ 点击登录按钮
    └─ 等待重定向到 /home
    └─ 返回登录结果
5. 验证：
    ✓ 登录后 URL 应该是 BASE_URL/home
    ✓ 页面标题应该包含项目名称
6. 保存 cookies 到浏览器上下文
7. 浏览器关闭时清理资源
```

### 4.2 验证点

**test_login_success**:
- ✓ 登录后 URL 包含 `/home`
- ✓ 页面标题不为空
- ✓ 页面加载完成（networkidle）

**后续补充**:
- ✓ 各角色登录后显示对应菜单（权限验证）
- ✓ 错误账号登录失败（负向测试）
- ✓ 会话超时自动退出（会话管理）

---

## 5. 依赖清单

### 5.1 主要依赖

| 包名 | 版本 | 用途 |
|------|------|------|
| pytest | ^7.4.0 | 测试框架 |
| pytest-playwright | ^0.4.0 | Playwright pytest 插件 |
| playwright | ^1.40.0 | 浏览器自动化 |
| python-dotenv | ^1.0.0 | .env 文件读取 |
| allure-pytest | ^2.13.2 | 测试报告 |

### 5.2 可选依赖

- `pytest-xdist` - 多进程并行测试
- `pytest-rerunfailures` - 失败重试
- `Pillow` - 截图对比

---

## 6. 测试范围（本阶段）

### 6.1 实现内容

- ✅ 登录功能测试（三角色参数化）
- ✅ 基础 POM 框架
- ✅ 环境配置系统
- ✅ 项目结构和占位符

### 6.2 不包含（后续补充）

- ❌ 权限验证（菜单可见性）
- ❌ 功能页测试
- ❌ 错误场景测试
- ❌ E2E 流程测试
- ❌ 性能/安全测试

---

## 7. 文件说明

### 7.1 要实现的核心文件

1. **conftest.py** (根级)
   - 初始化 Playwright chromium browser
   - 管理浏览器生命周期
   - 提供 `browser` fixture

2. **tests/conftest.py** (测试级)
   - 依赖根级 conftest
   - 提供 `account_type` 参数
   - 提供 `login_page` fixture

3. **pages/common/base_page.py**
   - Page Object 基类
   - 封装常用交互方法

4. **pages/common/login_page.py**
   - 继承 base_page
   - 实现 `login()` 方法

5. **tests/auth/test_login.py**
   - 参数化登录测试
   - 验证三个角色登录

6. **utils/config.py**
   - 读取 .env 文件
   - 管理 BASE_URL、账号等配置

7. **utils/logger.py**
   - 日志工具
   - 支持 fixture 中记录测试信息

8. **data/test_accounts.json**
   - 三个角色的账号数据

9. **pytest.ini**
   - pytest 配置（标记、输出路径、插件）

10. **requirements.txt**
    - 项目依赖清单

11. **.env.test.example**
    - 环境变量模板

---

## 8. 关键实现细节

### 8.1 浏览器初始化

```python
# conftest.py
browser = await chromium.launch(headless=False, slowMo=100)
```

- `headless=False` - 可见浏览器（便于调试）
- `slowMo=100` - 动作减速 100ms（便于观察）

### 8.2 等待策略

使用 Playwright 的标准等待策略：
- `waitForLoadState('networkidle')` - 网络空闲
- `waitForSelector(timeout)` - 元素出现
- `waitForURL()` - URL 匹配

### 8.3 错误处理

- Login 失败：抛出异常，终止测试
- 元素未找到：使用 wait 重试
- 网络超时：捕获异常，记录日志

---

## 9. 后续扩展计划

**Phase 2** - 权限与导航测试
- 验证各角色菜单可见性
- 测试权限边界（无权限页面访问）

**Phase 3** - 功能模块测试
- 项目管理（创建、编辑、发布）
- 报价管理（提交、议价、评标）
- 组织管理（机构、部门、员工）

**Phase 4** - E2E 业务流程
- 完整招标流程（创建→发布→报价→评标→中标）
- 多角色交互场景

---

## 10. 审批与版本控制

| 版本 | 日期 | 变更 | 审批 |
|------|------|------|------|
| 1.0 | 2026-04-09 | 初始设计 | ✅ 用户已批准 |

