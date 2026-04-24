"""
RFP 项目报价详情页 - 功能测试
测试场景: Operate 角色在详情页中添加内部跟进备注
"""

import pytest
import allure
from pages.operate.rfp_management.rfp_detailPage_project import RFPDetailPageProject
from utils.test_data_loader import TestDataLoader

# 加载参数化测试数据
test_cases = TestDataLoader.load_params("rfp_management_params.json", "rfp_detail_page")


@allure.feature("RFP 项目管理")
@allure.story("报价详情页 - 内部跟进备注测试")
class TestRFPDetailPageProject:
    """RFP 报价详情页功能测试类"""

    @pytest.mark.asyncio
    @pytest.mark.mark_20260507
    @pytest.mark.parametrize(
        "test_data",
        test_cases,
        ids=[tc["case_id"] for tc in test_cases]
    )
    @allure.title("报价详情页 - 添加内部跟进备注")
    @allure.description("""
    测试: Operate 角色在报价详情页中添加内部跟进备注并验证笔记是否保存

    登录状态复用：
    - 所有参数化用例共享同一登录状态（Module 级）
    - 首次执行 operate_user fixture 时登录一次
    - 后续用例复用此登录状态，无需重复登录
    - 提升测试执行效率

    测试步骤:
    1. 使用 operate 角色账号登录 (fixture 自动完成，仅一次)
    2. 导航至 Contracting 页面
    3. 选择 Started Tab
    4. 搜索项目（使用参数中的搜索关键词）
    5. 点击第一个项目的 Contract Signing 按钮
    6. 进入签约页面，选择 New proposal 标签页
    7. 选择第一个酒店
    8. 点击 Detail 按钮打开详情页弹窗
    9. 在详情页中，点击内部跟进备注按钮
    10. 添加备注内容: hy-自动化书写文字-{timestamp}
    11. 点击备注确定按钮保存
    12. 刷新详情页
    13. 验证备注内容是否保存成功

    预期结果: 备注内容保存成功，刷新后仍然可见
    """)
    async def test_add_internal_notes(self, page_module, operate_user, test_data):
        """
        参数化的详情页内部跟进备注存储测试（登录状态复用）

        Args:
            page_module: Module 级 page 对象 - 所有参数化用例共享（Module 级登录状态）
            operate_user: Operate 角色登录 fixture (来自 conftest.py)
            test_data: 参数化测试数据 (来自 rfp_management_params.json)
        """
        # 初始化 POM 类
        detail_page = RFPDetailPageProject(page_module)

        with allure.step(f"用例: {test_data['description']}"):
            # ========== Step 1-3: 导航到 Contracting 页面并选择 Started Tab ==========
            with allure.step("导航至 Contracting 页面"):
                await detail_page.navigate_to_contracting()
                await detail_page.click_started_tab()

            # ========== Step 4: 搜索项目 ==========
            with allure.step(f"搜索项目（关键词: {test_data['search_keyword']}）"):
                await detail_page.search_project_by_keyword(test_data['search_keyword'])

            # ========== Step 5: 点击 Contract Signing ==========
            with allure.step("点击 Contract Signing 按钮"):
                await detail_page.click_contract_signing()

            # ========== Step 6: 选择 New proposal 标签页 ==========
            with allure.step("选择 New proposal 标签页"):
                await detail_page.click_new_proposal_tab()

            # ========== Step 7: 选择第一个酒店 ==========
            with allure.step("选择第一个酒店"):
                await detail_page.select_first_hotel()

            # ========== Step 8: 点击 Detail 按钮打开详情页弹窗 ==========
            detail_popup = None
            with allure.step("点击 Detail 按钮"):
                detail_popup = await detail_page.click_detail_button()

            # ========== Step 9: 点击内部跟进备注按钮 ==========
            with allure.step("点击内部跟进备注按钮"):
                await detail_page.click_internal_notes_button(detail_popup)

            # ========== Step 10: 添加备注内容 ==========
            notes_content = None
            with allure.step("填写备注内容"):
                notes_content = await detail_page.fill_internal_notes(detail_popup)

            # ========== Step 11: 点击备注确定按钮 ==========
            with allure.step("点击备注确定按钮"):
                await detail_page.click_notes_confirm_button(detail_popup)

            # ========== Step 12: 刷新详情页 ==========
            with allure.step("刷新详情页"):
                await detail_page.refresh_detail_page(detail_popup)

            # ========== Step 13: 验证备注内容 ==========
            with allure.step("验证备注内容是否保存"):
                notes_saved = await detail_page.verify_notes_in_detail_page(detail_popup, notes_content)
                assert notes_saved, f"备注内容未保存：{notes_content}"

                allure.attach(
                    f"备注内容保存成功\n"
                    f"备注内容: {notes_content}",
                    "验证结果",
                    allure.attachment_type.TEXT
                )

            # ========== Step 14: 关闭详情页弹窗 ==========
            with allure.step("关闭详情页弹窗"):
                await detail_page.close_detail_page(detail_popup)

            # ========== Allure 最终报告 ==========
            allure.attach(
                f"详情页内部跟进备注测试成功\n"
                f"用例ID: {test_data['case_id']}\n"
                f"用例描述: {test_data['description']}\n"
                f"搜索关键词: {test_data['search_keyword']}\n"
                f"项目名称: {test_data['project_name']}\n"
                f"备注内容: {notes_content}\n"
                f"测试结果: 保存成功✓",
                "测试结果",
                allure.attachment_type.TEXT
            )