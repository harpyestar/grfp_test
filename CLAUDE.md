# 项目内容记录

## 角色定位
你是一名定位为专业测试专家，兼具需求分析与自主梳理能力，以质量保障为核心，深度衔接需求与测试全流程。可精准解读需求文档，快速提炼核心业务逻辑、功能点与约束条件，无需额外引导即可自主完成需求拆解、测试范围界定与用例思路梳理。既能从业务视角把控测试完整性，也能从技术角度识别潜在风险与异常场景，全程高效支撑测试设计、执行与质量评估工作，实现需求理解 — 测试规划 — 质量验证的闭环落地。

## 工作规范:
1. 当我提到：查看需求，请你到本项目目录下docs/需求描述.md
2. 项目结构和业务名词要好好理解到位，不理解的地方及时提问
2. 遇到测试失败，请立即停止
3. 把失败原因告诉我，让我来检查判定给出方向 
4. 不要自作主张修改代码，让我来鉴定
5. 询问用户，等待指示
6. 不要主张每一次都进行提交到git当中，只有当我要求提交git，你才进行提交到git

## 名词解释

### 系统角色定义
| 名词   | 描述                                                          |
|------|-------------------------------------------------------------|
| Operate（运营平台）  | 平台端角色，拥有较高的权限，可操作企业端所有内容，可参与中标和修改价格等                        |
| Enterprise（企业端）  | 企业端角色，拥有发布项目、招标功能，变动价格页签状态                                  |
| Hotel（单体酒店端）  | 酒店端角色，单店角色账号机构，可参与项目的竞标                                     |
| HotelGroup（酒店集团端） | 酒店集团端角色，旗下可关联多个品牌，以及品牌酒店，或单独关联某个酒店，可参与项目竞标，以及对旗下关联酒店的竞标价格审核 |

### 系统功能
### 1.1 系统核心功能模块

| 模块 | 功能概述                | 涉及角色 |
|------|---------------------|---------|
| 用户认证 | 登录、退出、密码重置、短信验证码    | 全部 |
| 首页工作台 | 说明展示                | 全部 |
| 项目管理（招标）| 项目创建、发布、启动、终止、作废    | Enterprise、Operate |
| 邀约酒店管理 | 邀请酒店、集团、批量操作        | Enterprise、Operate |
| 报价管理（酒店端）| 查看项目、提交报价、议价、拒绝     | Hotel、HotelGroup |
| 评标管理 | 查看报价详情、评标分析         | Enterprise、Operate |
| 机构管理 | 机构、部门、员工、签约主体管理     | 全部（权限范围不同） |
| POI 管理 | POI 绑定、解绑、地图配置      | Enterprise、Operate |
| 文件管理 | 文件上传、下载、附件关联        | 全部 |


### 1.2 核心业务流程

```
运营端 创建项目 → 填写多个Tab信息 → 启动项目（state: 0→1）
    ↓ 邀约酒店
酒店端 收到邀约 → 选房型+填报价 → 提交报价（bidState: 0→2）
    ↓ 
运营端 评标 → 查看报价详情 → 选定中签酒店
    ↓
项目归档完成（state: →2）
```


### 实现UI测试技术栈
python+Playwright（pytest-playwright）+allure

---

## ✅ 已完成：grfp-ui-test 项目搭建

### 项目状态
- **项目名称**: grfp-ui-test
- **位置**: `d:\work_dev\GRFP\grfp-ui-test\`
- **Git 标签**: v1.0.0
- **提交数**: 14 个语义化提交
- **测试用例**: 9 个 (3 个测试方法 × 3 个角色参数化)
- **状态**: ✅ 完整项目骨架 + 登录功能实现完成

### 实际项目目录结构（已实现）

```
grfp-ui-test/
├── .env                              # 本地环境配置
├── .gitignore                        # git 忽略规则
├── CLAUDE.md                         # 项目内容记录与指导
├── IMPLEMENTATION_SUMMARY.md         # 项目实现总结
├── conftest.py                       # 根级 conftest（浏览器生命周期管理）
├── pytest.ini                        # pytest 全局配置
├── requirements.txt                  # 项目依赖（pytest, playwright, allure...）
├── run.py                            # 测试运行脚本
├── explore_rfp_form.py               # 表单页面探索脚本
│
├── docs/                             # 文档目录
│   ├── DESIGN.md                     # 项目设计文档
│   ├── IMPLEMENTATION_PLAN.md        # 实现计划文档
│   ├── README.md                     # 项目使用文档
│   ├── 需求描述.md                   # 业务需求文档
│   ├── 文件记录/                     # 对话历史记录
│   │   └── 2026年4月23日-对话记录
│   └── superpowers/                  # 超级能力相关文件
│       ├── plans/
│       │   └── 2026-04-10-create-rfp-project-plan.md
│       └── specs/
│           └── 2026-04-10-create-rfp-project-design.md
│
├── pages/                            # Page Object Models（按角色分类）
│   ├── __init__.py
│   ├── common/
│   │   ├── __init__.py
│   │   ├── base_page.py              # ✅ POM 基类（11 个通用交互方法）
│   │   └── login_page.py             # ✅ 登录页 POM
│   │
│   ├── operate/                      # ✅ 运营端功能页
│   │   ├── __init__.py
│   │   ├── admin/
│   │   ├── ai_import/
│   │   ├── organization/
│   │   ├── poi_management/
│   │   └── rfp_management/
│   │       ├── __init__.py
│   │       └── create_rfp_project_page.py  # ✅ RFP 项目创建页 POM
│   │
│   ├── hotel/                        # 酒店端功能页
│   │   ├── __init__.py
│   │   ├── contracting/
│   │   ├── home/
│   │   ├── organization/
│   │   ├── system_config/
│   │   └── user_management/
│   │
│   └── hotel_group/                  # 酒店集团端功能页
│       ├── __init__.py
│       ├── contracting/
│       ├── home/
│       ├── menu_permission/
│       ├── organization/
│       └── user_management/
│
├── tests/                            # 测试用例
│   ├── __init__.py
│   ├── conftest.py                   # 测试级配置（参数化、fixtures）
│   │
│   ├── auth/                         # 认证测试
│   │   ├── __init__.py
│   │   └── test_login.py             # ✅ 登录测试（9 个用例: 3 角色 × 3 操作）
│   │
│   ├── operate/                      # 运营端测试
│   │   ├── __init__.py
│   │   ├── admin/
│   │   ├── organization/
│   │   └── rfp_management/
│   │       ├── __init__.py
│   │       ├── conftest.py           # ✅ RFP 管理测试配置
│   │       └── test_create_rfp_project.py  # ✅ RFP 项目创建测试
│   │
│   ├── hotel/                        # 酒店端测试
│   │   ├── __init__.py
│   │   ├── contracting/
│   │   ├── home/
│   │   ├── organization/
│   │   ├── system_config/
│   │   └── user_management/
│   │
│   ├── hotel_group/                  # 酒店集团端测试
│   │   ├── __init__.py
│   │   ├── contracting/
│   │   ├── home/
│   │   ├── menu_permission/
│   │   ├── organization/
│   │   └── user_management/
│   │
│   └── e2e/                          # 端到端测试
│       └── __init__.py
│
├── data/                             # 数据管理
│   ├── __init__.py
│   ├── test_accounts.json            # ✅ 三角色账号数据
│   ├── fixtures/
│   │   ├── __init__.py
│   │   └── accounts.py               # ✅ pytest fixtures
│   └── test_cases/
│       ├── __init__.py
│       └── rfp_management_params.json # ✅ RFP 管理参数化数据
│
├── utils/                            # 工具函数
│   ├── __init__.py
│   ├── config.py                     # ✅ 配置管理（.env + test_accounts.json）
│   ├── logger.py                     # ✅ 日志工具（Logger 单例）
│   ├── test_data_loader.py           # ✅ 参数化测试数据加载器
│   ├── timeout_config.py             # ✅ 超时配置管理类
│   └── wait_helper.py                # ✅ 等待工具（异步 Playwright 等待）
│
└── reports/                          # 测试报告
    ├── .gitkeep
    ├── allure-results/               # Allure 报告输出
    │   └── .gitkeep
    └── logs/                         # 测试日志
        └── .gitkeep
```

### 关键设计特点

| 特性 | 说明 |
|------|------|
| 会话复用 | 浏览器 session 级复用，减少重复登录 |
| 参数化测试 | 同一测试代码自动运行 3 个角色（operate, hotel, hotelgroup） |
| 环境管理 | 支持 test/pre/prod 环境切换（.env 文件） |
| 异步支持 | 完整的 Playwright async/await 集成 |
| POM 模式 | 清晰的 Page Object Model 分层 |
| 详细日志 | Logger 单例模式，便于调试 |

---

## 📋 项目演进记录

### 已实现功能清单

| 功能模块 | 状态 | 说明 |
|---------|------|------|
| **基础框架** | ✅ | POM 基类、conftest、pytest 配置、日志系统 |
| **认证功能** | ✅ | 登录页面、三角色登录测试（9 个用例参数化） |
| **RFP 项目管理** | ✅ | 创建 RFP 项目页面 POM、创建流程测试用例、参数化测试数据加载 |
| **超时管理** | ✅ | 统一超时配置、避免硬编码 |
| **元素定位规范** | ✅ | 定位器集中管理、支持多种定位方式 |
| **参数化测试数据** | ✅ | test_accounts.json（角色账户）、rfp_management_params.json（RFP 参数） |
| **文档系统** | ✅ | 需求描述、设计文档、实现计划、使用指南 |

### 待实现功能

| 功能模块 | 优先级 | 备注 |
|---------|------|------|
| 邀约酒店管理页面与测试 | P1 | 需要实现页面 POM 和对应测试 |
| 报价管理页面与测试 | P1 | 酒店端提交报价流程 |
| 评标管理页面与测试 | P1 | 运营端查看报价和评标 |
| 机构管理页面与测试 | P2 | 组织、部门、员工、签约主体管理 |
| POI 管理页面与测试 | P2 | POI 绑定、解绑、地图配置 |
| 系统配置页面与测试 | P2 | 系统参数配置 |
| 端到端测试 | P3 | 完整业务流程串联测试 |

---

## 系统页面结构与导航

### 角色菜单权限

登录后，系统首页为 `/home`，不同角色可见的菜单模块不同。

| 菜单模块 | Operate | Hotel | HotelGroup |
|---------|---------|-------|------------|
| Work table | ✅ | ✅ | ✅ |
| Contracting | ✅ | ✅ | ✅ |
| Create new RFP project | ✅ | ❌ | ❌ |
| AI Intelligent Import | ✅ | ❌ | ❌ |
| Hotel Bidding Management | ✅ | ❌ | ❌ |
| Org Management | ✅ | ✅ | ✅ |
| User Management | ✅ | ✅ | ✅ |
| POI Management | ✅ | ❌ | ❌ |
| MENU GROUP USER MANAGEMENT | ✅ | ❌ | ✅ |
| System Config | ✅ | ✅ | ❌ |
| Other Management | ✅ | ❌ | ❌ |

### 页面交互特征

- **前端框架**：Vue.js（动态渲染）
- **UI 组件库**：Element UI (El-* 组件)
- **主要组件**：侧边栏导航、下拉菜单、抽屉面板、模态对话框、表格/列表、表单

---


## 🔧 超时配置管理规则

**核心原则：禁止硬编码超时值，所有超时配置统一管理**

- 超时配置定义在 `.env.test`：`TIMEOUT_PAGE_LOAD`、`TIMEOUT_ELEMENT`、`TIMEOUT_NAVIGATION`
- 通过 `utils/timeout_config.py` 统一读取，仅此一处与 `.env` 交互
- 代码中使用：`from utils.timeout_config import timeout_config; timeout_config.get_element_timeout()`
- 不要在每个文件中重复读取 `.env`，不要在代码中硬编码任何超时数值（如 `timeout=10000`）
- 新建 Page Object 或工具类时，直接从 `timeout_config` 获取超时值，不创建新常量

---

## 元素定位规则

** 所有的元素单独放出来，禁止硬编程，便于后续调成 **

我需要用 Playwright 精准定位页面表单元素（输入框/单选/复选/下拉框/提交按钮），请严格按照以下规则执行，禁止使用脆弱定位方式：

=== 核心定位规则（必须遵守） ===
1. 优先使用最稳定的定位器：
   ① 文本定位（最通用）：page.getByRole('button', { name: /提交|确认|登录|搜索/i })
   ② 标签关联定位（输入框专用）：page.getByLabel('用户名') / page.getByPlaceholder('请输入手机号')
   ③ 测试属性定位（最稳定）：page.getByTestId('submit-btn')
   ④ 表单name属性：page.locator('[name="username"]')
2. 绝对禁止使用：动态id、随机class、长链式css选择器、xpath绝对路径
3. 必须检查：iframe嵌套、shadow DOM、元素隐藏、动态加载、弹窗表单
4. 必须输出：可直接运行的代码 + 定位验证方法 + 失败排查方案


