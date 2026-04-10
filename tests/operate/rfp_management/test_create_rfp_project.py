"""
创建新 RFP 项目 - 功能测试
测试场景: Operate 角色完整创建 RFP 项目流程
"""

import pytest
import allure
from pages.operate.rfp_management.create_rfp_project_page import CreateNewRFPProjectPage


@allure.feature("RFP 项目管理")
@allure.story("创建新 RFP 项目")
class TestCreateRFPProject:
    """RFP 项目创建功能测试类"""

    @pytest.mark.asyncio
    @allure.title("创建新 RFP 项目 - 完整流程")
    @allure.description("""
    测试: Operate 角色成功创建新 RFP 项目，填写所有必填字段并保存

    测试步骤:
    1. 使用 operate 角色账号登录 (fixture 自动完成)
    2. 导航至 Create new RFP project 页面
    3. 填写项目基本信息 (组织、项目名、联系人、电话)
    4. 选择签约方式和通知方式
    5. 设置报价报告为 "NO NEED"
    6. 选择三个日期范围 (2026-04-10 ~ 2026-05-10)
    7. 填写预期酒店数量 (随机)
    8. 点击保存
    9. 断言成功提示出现

    预期结果: 保存成功，显示成功提示信息
    """)
    async def test_create_rfp_project_success(self, page, operate_user):
        """
        完整的 RFP 项目创建流程测试

        Args:
            page: Playwright Page 对象 (fixture 提供)
            operate_user: Operate 角色登录 fixture (来自 conftest.py)
        """
        # 初始化 POM 类
        create_page = CreateNewRFPProjectPage(page)

        # Step 1: 导航至创建页面
        await create_page.navigate_to_create_rfp()

        # Step 2: 填写基本信息
        await create_page.fill_organization_name("hyg测试机构")
        project_name = await create_page.fill_project_name()
        await create_page.fill_contact_person("荷叶")
        await create_page.fill_contact_number("010", "12345678")

        # Step 3: 选择方式
        await create_page.select_signing_method()
        await create_page.select_notification_method()

        # Step 4: 设置报价报告
        await create_page.handle_quotation_reports()

        # Step 5: 选择日期范围
        await create_page.select_bidding_dates("2026-04-10", "2026-05-10")

        # Step 6: 填写酒店数量
        hotels_count = await create_page.fill_expected_hotels_count()

        # Step 7: 点击保存
        await create_page.click_save_button()

        # Step 8: 验证成功
        success = await create_page.verify_save_success()

        # Assertion
        assert success, "保存成功提示未出现，项目创建失败"

        # Allure 最终报告
        allure.attach_text(
            f"项目创建成功\n"
            f"项目名称: {project_name}\n"
            f"预期酒店数: {hotels_count}",
            "测试结果"
        )

    @pytest.mark.asyncio
    @allure.title("创建新 RFP 项目 - 验证必填字段")
    async def test_create_rfp_project_verify_required_fields(self, page, operate_user):
        """
        测试验证所有必填字段都已正确填写

        预期结果: 所有字段都能被正确填充
        """
        create_page = CreateNewRFPProjectPage(page)

        with allure.step("导航至创建页面"):
            await create_page.navigate_to_create_rfp()

        with allure.step("验证必填字段都能填充"):
            # 填写组织名称
            await create_page.fill_organization_name("hyg测试机构")
            allure.attach_text("✓ 组织名称字段可填充", "字段验证")

            # 填写项目名称
            project_name = await create_page.fill_project_name()
            assert project_name.startswith("hyg-自动化项目-"), "项目名称格式错误"
            allure.attach_text(f"✓ 项目名称字段可填充: {project_name}", "字段验证")

            # 填写联系人
            await create_page.fill_contact_person("荷叶")
            allure.attach_text("✓ 联系人字段可填充", "字段验证")

            # 填写电话
            await create_page.fill_contact_number("010", "12345678")
            allure.attach_text("✓ 联系电话字段可填充", "字段验证")

        allure.attach_text("所有必填字段验证通过", "测试结果")
