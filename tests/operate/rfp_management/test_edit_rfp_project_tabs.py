"""
编辑 RFP 项目 Tab 保存功能测试
测试场景: 验证 RFP 项目编辑页面中每个 Tab 的保存功能是否成功
"""
import time

import pytest
import allure
from pages.operate.rfp_management.edit_rfp_project_page import EditRFPProjectPage
from utils.test_data_loader import TestDataLoader

lra_nlra_prompt_cases = TestDataLoader.load_params(
    "rfp_management_params.json", "rfp_lra_nlra_prompt_options"
)


@allure.feature("RFP 项目管理")
@allure.story("RFP 项目编辑 - Tab 保存功能")
class TestEditRFPProjectTabs:
    """RFP 项目编辑页面 Tab 保存功能测试类"""

    # 固定的项目名称（需要在系统中存在）
    TEST_PROJECT_NAME = "hyg-自动化项目-未完成项"

    @pytest.mark.asyncio
    @allure.title("验证 RFP 项目编辑页面中所有 Tab 的保存功能")
    @allure.description("""
    测试: Operate 角色在 RFP 项目编辑页面中验证每个 Tab 的保存功能是否正常

    测试流程:
    1. 使用 operate 角色账号登录 (fixture 自动完成)
    2. 导航至 RFP Management > Contracting 页面
    3. 选择 "Not Started" Tab
    4. 搜索固定项目名: hyg-自动化项目-未完成项
    5. 点击 Modify Project 进入编辑页面
    6. 遍历编辑页面的所有 Tab:
       - 对有 Save 按钮的 Tab: 点击 Save → 验证成功提示出现
       - 对无 Save 按钮的 Tab: 正常跳过
    7. 生成完整的测试结果报告

    预期结果:
    - 所有有 Save 按钮的 Tab 保存成功，显示成功提示
    - 所有无 Save 按钮的 Tab 正常处理
    """)
    async def test_edit_rfp_project_all_tabs_save(self, page_module, operate_user):
        """
        完整的 RFP 项目编辑页面 Tab 保存功能测试

        Args:
            page_module: Module 级 page 对象 - 复用登录状态
            operate_user: Operate 角色登录 fixture
        """
        # 初始化 POM 类
        edit_page = EditRFPProjectPage(page_module)

        with allure.step("【步骤 1】导航至 RFP Management > Contracting 页面"):
            # 导航至 Contracting 页面
            await edit_page.navigate_to_contracting()

        with allure.step("【步骤 2】选择 Not Started Tab"):
            # 选择 Not Started Tab
            await edit_page.click_not_started_tab()

        with allure.step(f"【步骤 3】搜索项目: {self.TEST_PROJECT_NAME}"):
            # 搜索项目并打开编辑页面
            await edit_page.search_and_open_project(self.TEST_PROJECT_NAME)

        with allure.step("【步骤 4】遍历所有 Tab 进行保存功能测试"):
            # 执行完整的 Tab 保存功能测试
            test_results = await edit_page.test_all_tabs_save_functionality()

        with allure.step("【步骤 5】验证测试结果"):
            # 基本的断言检查
            # 检查是否测试了所有的 Tab
            assert test_results["total_tabs"] > 0, "未能获取到任何 Tab"

            # 检查总 Tab 数是否与预期相符
            total_processed = test_results["tabs_with_save"] + test_results["tabs_without_save"]
            assert total_processed == test_results["total_tabs"], \
                f"处理的 Tab 数 ({total_processed}) 与总 Tab 数 ({test_results['total_tabs']}) 不符"

            # 检查是否所有有 Save 按钮的 Tab 都保存成功
            total_save_operations = test_results["save_success_count"] + test_results["save_failure_count"]
            assert total_save_operations == test_results["tabs_with_save"], \
                f"Save 操作数 ({total_save_operations}) 与有 Save 按钮的 Tab 数 ({test_results['tabs_with_save']}) 不符"

            # 检查是否所有有 Save 按钮的 Tab 都成功保存
            if test_results["save_failure_count"] > 0:
                failed_tabs = [
                    d["tab_name"] for d in test_results["details"]
                    if d["has_save"] and d["save_result"] != "SUCCESS"
                ]
                assert False, f"以下 Tab 保存失败: {', '.join(failed_tabs)}"

        # 生成最终的 Allure 报告
        final_report = f"""
        [OK] RFP 项目编辑页面 Tab 保存功能测试完成
        
        【测试项目】
        - 项目名称: {self.TEST_PROJECT_NAME}
        
        【测试统计】
        - 总 Tab 数: {test_results['total_tabs']}
        - 有 Save 按钮的 Tab: {test_results['tabs_with_save']}
        - 无 Save 按钮的 Tab: {test_results['tabs_without_save']}
        - 保存成功: {test_results['save_success_count']}/{test_results['tabs_with_save']}
        - 保存失败: {test_results['save_failure_count']}/{test_results['tabs_with_save']}
        
        【测试覆盖的 Tab】
        """
        for i, detail in enumerate(test_results["details"], 1):
            status_icon = "[OK]" if detail["save_result"] == "SUCCESS" else \
                         "[SKIP]" if detail["save_result"] == "NO_SAVE_BUTTON" else "[FAIL]"
            final_report += f"\n{i}. {status_icon} {detail['tab_name']}"
            final_report += f"\n   - 状态: {detail['save_result']}"
            final_report += f"\n   - 说明: {detail['message']}"

        allure.attach(final_report, "完整测试报告", allure.attachment_type.TEXT)

    @pytest.mark.asyncio
    @allure.title("验证未启动项目的 Start 按钮和确认弹窗")
    @allure.description("""
    测试: Operate 角色在 Contracting 页面中查看未启动项目的 Start 按钮和确认弹窗

    测试流程:
    1. 使用 operate 角色账号登录 (fixture 自动完成)
    2. 导航至 RFP Management > Contracting 页面
    3. 选择 "Started" Tab
    4. 搜索未启动项目: hyg-自动化项目-未完成项
    5. 点击该项目的 Start 按钮
    6. 验证 Yes 确认按钮出现（不点击 Yes，只验证出现）

    预期结果:
    - 能够找到项目的 Start 按钮
    - 点击 Start 后出现 Yes 确认按钮的弹窗
    """)
    async def test_verify_start_project_confirmation_popup(self, page_module, operate_user):
        """
        验证未启动项目的 Start 按钮和确认弹窗

        Args:
            page_module: Module 级 page 对象 - 复用登录状态
            operate_user: Operate 角色登录 fixture
        """
        # 初始化 POM 类
        edit_page = EditRFPProjectPage(page_module)

        with allure.step("【步骤 1】导航至 RFP Management > Contracting 页面"):
            # 导航至 Contracting 页面
            await edit_page.navigate_to_contracting()

        with allure.step("【步骤 2】选择 Not Started Tab"):
            # 选择 Not Started Tab
            await edit_page.click_not_started_tab()

        with allure.step(f"【步骤 3】搜索项目: {self.TEST_PROJECT_NAME}"):
            # 搜索项目
            await edit_page.search_project_by_keyword(self.TEST_PROJECT_NAME)

        with allure.step("【步骤 4】点击 Start 按钮"):
            # 点击 Start 按钮
            await edit_page.click_start_button()

        with allure.step("【步骤 5】验证 Yes 确认按钮出现"):
            # 验证确认弹窗是否显示
            confirmation_visible = await edit_page.verify_start_confirmation_popup_visible()
            assert confirmation_visible, "Start 确认弹窗（Yes 按钮）未出现"

        # 生成测试结果报告
        result_report = f"""
        [OK] 未启动项目 Start 按钮验证测试完成

        【测试项目】
        - 项目名称: {self.TEST_PROJECT_NAME}

        【测试结果】
        - Start 按钮: 已找到并点击
        - 确认弹窗: 已出现（Yes 按钮可见）
        - 测试状态: 通过 ✓
        """
        allure.attach(result_report, "测试结果", allure.attachment_type.TEXT)

    @pytest.mark.asyncio
    @pytest.mark.mark_20260507
    @pytest.mark.parametrize(
        "test_data",
        lra_nlra_prompt_cases,
        ids=[tc["case_id"] for tc in lra_nlra_prompt_cases]
    )
    @allure.title("验证修改项目基础信息页 LRA/NLRA 提示选项")
    @allure.description("""
    测试: Operate 角色在修改项目基础信息页中校验
    "Prompt when both LRA and NLRA quotes are successful" 仅存在 turn off 和 turn on 两个选项

    测试流程:
    1. 使用 operate 角色账号登录 (fixture 自动完成)
    2. 导航至 RFP Management > Contracting 页面
    3. 选择 Started Tab
    4. 搜索参数化项目名
    5. 点击首个 Modify Project 进入编辑页面
    6. 在基础信息页读取 LRA/NLRA 提示项的所有单选文本
    7. 断言选项顺序和内容仅为 turn off、turn on

    预期结果:
    - 页面仅展示 turn off 和 turn on 两个选项
    - 不存在重复选项或额外选项
    """)
    async def test_verify_lra_nlra_prompt_options(self, page_module, operate_user, test_data):
        """验证修改项目基础信息页 LRA/NLRA 提示项只包含两个预期选项"""
        edit_page = EditRFPProjectPage(page_module)

        with allure.step("【步骤 1】导航至 RFP Management > Contracting 页面"):
            await edit_page.navigate_to_contracting()

        with allure.step(f"【步骤 2】选择 {test_data['contracting_tab']} Tab"):
            await edit_page.click_started_tab()

        with allure.step(f"【步骤 3】搜索项目: {test_data['project_name']}"):
            await edit_page.search_project_by_keyword(test_data['project_name'])

        with allure.step("【步骤 4】进入首个 Modify Project 编辑页"):
            await edit_page.open_modify_project_from_search_result()

        with allure.step("【步骤 5】校验 LRA/NLRA 提示项"):
            verification_result = await edit_page.verify_lra_nlra_prompt_options(
                test_data['expected_options']
            )

            assert verification_result["actual_count"] == len(test_data["expected_options"]), \
                f"LRA/NLRA 选项数量不正确: {verification_result['actual_options']}"
            assert verification_result["unique_count"] == len(test_data["expected_options"]), \
                f"LRA/NLRA 选项存在重复: {verification_result['actual_options']}"
            assert verification_result["is_match"], \
                f"LRA/NLRA 选项不符合预期，实际: {verification_result['actual_options']}"

        # 生成测试结果报告
        result_report = f"""
        [OK] LRA/NLRA 提示项验证完成

        【测试项目】
        - 项目名称: {test_data['project_name']}
        - Contracting Tab: {test_data['contracting_tab']}

        【验证结果】
        - 实际选项: {verification_result['actual_options']}
        - 期望选项: {verification_result['expected_options']}
        - 数量校验: {verification_result['actual_count']}
        - 去重校验: {verification_result['unique_count']}
        - 测试状态: 通过 ✓
        """
        allure.attach(result_report, "测试结果", allure.attachment_type.TEXT)
