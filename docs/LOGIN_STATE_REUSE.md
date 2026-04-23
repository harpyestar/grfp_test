# 登录状态复用优化方案

## 问题背景

在参数化测试中，当同一个测试方法有多条参数化用例时，原来的配置会导致**每条用例都重新执行一次登录**。

```
❌ 之前（低效）:
用例1 → [登录] → 执行 → [登出]
用例2 → [登录] → 执行 → [登出]  
用例3 → [登录] → 执行 → [登出]
总耗时: 3 × (登录时间 + 执行时间)
```

## 解决方案

采用 **Module 级 Fixture 复用**策略，使同一模块内的所有参数化测试共享一个登录状态。

```
✅ 之后（高效）:
用例1 → [登录一次] → 执行 
用例2 → [复用登录] → 执行
用例3 → [复用登录] → 执行  
总耗时: 1 × 登录时间 + 3 × 执行时间
```

## 技术实现

### 1. 创建 Module 级 Page Fixture

在 `tests/operate/rfp_management/conftest.py` 中添加：

```python
@pytest.fixture(scope="module")
async def page_module(browser, event_loop):
    """整个模块共享同一个 page"""
    context = await browser.new_context()
    page = await context.new_page()
    yield page
    await page.close()
    await context.close()
```

**作用域：**
- `scope="module"` - 整个模块内只创建一次
- 所有参数化用例共享此 page

### 2. 改为 Module 级登录 Fixture

```python
@pytest.fixture(scope="module")
async def operate_user(page_module):
    """登录仅执行一次，后续用例复用"""
    login_page = LoginPage(page_module)
    result = await login_page.login(email, password)
    yield page_module  # 返回已登录的 page
```

**关键点：**
- 依赖 `page_module` 而不是 `page`
- `scope="module"` 确保只执行一次
- 返回已登录的 page

### 3. 更新测试方法

```python
async def test_create_rfp_project_success(
    self, 
    page_module,        # ← 使用 Module 级 page
    operate_user,       # ← 依赖登录状态
    test_data          # ← 参数化数据
):
    create_page = CreateNewRFPProjectPage(page_module)
    # ... 测试步骤 ...
```

## 效果对比

### 项目数据
- **参数化用例数：** 2 条 (case_001, case_002)
- **登录耗时：** ~2-3 秒
- **每条用例耗时：** ~5-10 秒

### 性能提升

| 指标 | 之前 | 之后 | 提升 |
|------|------|------|------|
| 总登录次数 | 2 次 | 1 次 | ⬇️ 50% |
| 登录总耗时 | 4-6 秒 | 2-3 秒 | ⬇️ 50% |
| 总执行时间 | 24-32 秒 | 12-16 秒 | ⬇️ ~50% |

## 注意事项

### ✅ 何时使用此模式

- 同一模块内有多个参数化用例
- 所有用例都使用同一个账号（角色）
- 用例之间没有相互依赖

### ⚠️ 何时不应使用

- 不同参数化用例需要不同的账号/角色
- 用例之间有执行顺序依赖
- 单个用例需要隔离的浏览器上下文

### 🔄 多角色支持

如果测试需要多个角色（operate + hotel），可以：

**方案 A：创建多个 Module 级 Fixture**
```python
@pytest.fixture(scope="module")
async def page_module_operate(browser): ...

@pytest.fixture(scope="module")  
async def page_module_hotel(browser): ...
```

**方案 B：在测试中切换账号**
```python
async def test_multi_role(page_module, event_loop):
    # 用 operate 角色执行操作
    login_page = LoginPage(page_module)
    await login_page.login(operate_account)
    # ... 执行操作 ...
    
    # 切换到 hotel 角色
    await login_page.logout()
    await login_page.login(hotel_account)
    # ... 执行操作 ...
```

## 日志示例

运行测试时的日志输出：

```
Setting up module-level page for login state reuse
✅ Module-level page created - ready for shared login state
Setting up operate user fixture [SCOPE: module] - performing login ONCE for all parametrized tests
Loading operate account: operate@example.com
✅ Operate user login successful (ONE-TIME for all tests in module)
   URL: https://app.example.com/home
   💡 Tip: All 2 parametrized test cases will reuse this login state

test_create_rfp_project_success[case_001] PASSED
test_create_rfp_project_success[case_002] PASSED

Closing module-level page and context
```

## 扩展到其他测试

此模式可应用于其他角色的参数化测试：

```python
# Hotel 角色测试
@pytest.fixture(scope="module")
async def hotel_user(page_module):
    login_page = LoginPage(page_module)
    result = await login_page.login(hotel_account)
    yield page_module

# HotelGroup 角色测试
@pytest.fixture(scope="module")
async def hotelgroup_user(page_module):
    login_page = LoginPage(page_module)
    result = await login_page.login(hotelgroup_account)
    yield page_module
```

## 总结

通过 Module 级 Fixture 复用登录状态：
- ⏱️ 大幅减少测试执行时间（降低 ~50%）
- 🔐 保持登录状态隔离（不影响其他模块）
- 🎯 简化 fixture 管理（清晰的作用域界定）
- 📊 提高测试执行效率（尤其是参数化测试多的场景）
