"""
创建新 RFP 项目 - 功能测试
测试场景: Operate 角色完整创建 RFP 项目流程
"""

import pytest
import allure
from pages.operate.rfp_management.create_rfp_project_page import CreateNewRFPProjectPage
from utils.test_data_loader import TestDataLoader

# 加载参数化测试数据
test_cases = TestDataLoader.load_params("rfp_management_params.json", "create_rfp_project")


@allure.feature("RFP 项目管理")
@allure.story("创建新 RFP 项目")
class TestCreateRFPProject:
    """RFP 项目创建功能测试类"""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "test_data",
        test_cases,
        ids=[tc["case_id"] for tc in test_cases]
    )
    @allure.title("创建新 RFP 项目 - 完整流程")
    @allure.description("""
    测试: Operate 角色成功创建新 RFP 项目，填写所有必填字段并保存

    登录状态复用：
    - 所有参数化用例共享同一登录状态（Module 级）
    - 首次执行 operate_user fixture 时登录一次
    - 后续用例复用此登录状态，无需重复登录
    - 提升测试执行效率

    测试步骤:
    1. 使用 operate 角色账号登录 (fixture 自动完成，仅一次)
    2. 导航至 Create new RFP project 页面
    3. 填写项目基本信息 (组织、项目名、联系人、电话)
    4. 选择签约方式和通知方式
    5. 设置报价报告为 "NO NEED"
    6. 选择三个日期范围
    7. 填写预期酒店数量
    8. 点击保存
    9. 断言成功提示出现

    预期结果: 保存成功，显示成功提示信息
    """)
    async def test_create_rfp_project_success(self, page_module, operate_user, test_data):
        """
        参数化的 RFP 项目创建流程测试（登录状态复用）

        Args:
            page_module: Module 级 page 对象 - 所有参数化用例共享（Module 级登录状态）
            operate_user: Operate 角色登录 fixture (来自 conftest.py)
            test_data: 参数化测试数据 (来自 rfp_management_params.json)
        """
        # 初始化 POM 类
        create_page = CreateNewRFPProjectPage(page_module)

        with allure.step(f"用例: {test_data['description']}"):
            # Step 1: 导航至创建页面
            await create_page.navigate_to_create_rfp()

            # Step 2: 填写基本信息
            await create_page.fill_organization_name(test_data["organization"])
            project_name = await create_page.fill_project_name()
            await create_page.fill_contact_person(test_data["contact_person"])
            await create_page.fill_contact_number(test_data["area_code"], test_data["phone"])

            # Step 3: 选择方式
            await create_page.select_signing_method()
            await create_page.select_notification_method()

            # Step 4: 设置报价报告
            await create_page.handle_quotation_reports()

            # Step 5: 选择日期范围
            await create_page.select_bidding_dates(test_data["start_date"], test_data["end_date"])

            # Step 6: 填写酒店数量（使用参数中的值）
            hotels_count = await create_page.fill_expected_hotels_count(test_data["expected_hotels"])

            # Step 7: 点击保存
            await create_page.click_save_button()

            # Step 8: 验证成功
            success = await create_page.verify_save_success()

            # Assertion
            assert success, "保存成功提示未出现，项目创建失败"

            # Allure 最终报告
            allure.attach(
                f"项目创建成功\n"
                f"用例ID: {test_data['case_id']}\n"
                f"用例描述: {test_data['description']}\n"
                f"项目名称: {project_name}\n"
                f"预期酒店数: {test_data['expected_hotels']}\n"
                f"日期范围: {test_data['start_date']} ~ {test_data['end_date']}",
                "测试结果",
                allure.attachment_type.TEXT
            )

        # ========== 清理数据部分：删除创建的项目 ==========
        with allure.step(f"清理数据：删除项目 {project_name}"):
            try:
                # 调用 POM 中的完整删除方法
                await create_page.delete_project_by_name(project_name)

                # Allure 清理报告
                allure.attach(
                    f"数据清理成功\n"
                    f"删除项目: {project_name}\n"
                    f"操作: Void\n"
                    f"状态: 已确认",
                    "清理结果",
                    allure.attachment_type.TEXT
                )

            except Exception as e:
                error_msg = f"清理数据失败: {str(e)}"
                allure.attach(
                    f"清理数据失败\n"
                    f"项目名称: {project_name}\n"
                    f"错误: {error_msg}",
                    "清理失败",
                    allure.attachment_type.TEXT
                )
                raise

