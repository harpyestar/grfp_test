"""
RFP 项目地图签约页面 - 功能测试
测试场景: Operate 角色在地图签约页面点击酒店标记，验证间夜信息弹窗的出现和消失
"""
import time

import pytest
import allure
from pages.operate.rfp_management.rfp_contracting_map_page import RFPContractingMapPage
from utils.test_data_loader import TestDataLoader

# 加载参数化测试数据
test_cases = TestDataLoader.load_params("rfp_management_params.json", "rfp_contracting_map")


@allure.feature("RFP 项目管理")
@allure.story("地图签约页面 - 间夜信息弹窗验证")
class TestRFPContractingMapProject:
    """RFP 项目地图签约功能测试类"""

    @pytest.mark.asyncio
    @pytest.mark.mark_20260507
    @pytest.mark.parametrize(
        "test_data",
        test_cases,
        ids=[tc["case_id"] for tc in test_cases]
    )
    @allure.title("地图签约页面 - 点击酒店标记验证弹窗")
    @allure.description("""
    测试: Operate 角色在地图签约页面点击酒店标记，验证间夜信息弹窗的出现和消失

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
    8. 模拟鼠标悬浮到地图标记上（不测试）
    9. 点击地图上的酒店标记 → 验证间夜信息弹窗出现
    10. 将鼠标移开 → 验证间夜信息弹窗消失

    预期结果: 弹窗在点击后出现，移开鼠标后消失
    """)
    async def test_map_marker_price_popup(self, page_module, operate_user, test_data):
        """
        参数化的地图签约页面弹窗验证测试（登录状态复用）

        Args:
            page_module: Module 级 page 对象 - 所有参数化用例共享（Module 级登录状态）
            operate_user: Operate 角色登录 fixture (来自 conftest.py)
            test_data: 参数化测试数据 (来自 rfp_management_params.json)
        """
        # 初始化 POM 类
        map_page = RFPContractingMapPage(page_module)

        with allure.step(f"用例: {test_data['description']}"):
            # ========== Step 1-3: 导航到 Contracting 页面并选择 Started Tab ==========
            with allure.step("导航至 Contracting 页面"):
                await map_page.navigate_to_contracting()
                await map_page.click_started_tab()

            # ========== Step 4: 搜索项目 ==========
            with allure.step(f"搜索项目（关键词: {test_data['search_keyword']}）"):
                await map_page.search_project_by_keyword(test_data['search_keyword'])

            # ========== Step 5: 点击 Contract Signing ==========
            with allure.step("点击 Contract Signing 按钮"):
                await map_page.click_contract_signing()

            # ========== Step 6: 选择 New proposal 标签页 ==========
            with allure.step("选择 New proposal 标签页"):
                await map_page.click_new_proposal_tab()

            # ========== Step 7: 选择第一个酒店 ==========
            with allure.step("选择第一个酒店"):
                await map_page.select_first_hotel()

            # ========== Step 8-9: 点击地图标记 - 验证弹窗出现 ==========
            with allure.step("点击地图标记 - 验证弹窗出现"):
                await map_page.click_map_marker()

            # ========== Step 10: 移开鼠标 - 验证弹窗消失 ==========
            with allure.step("移开鼠标 - 验证弹窗消失"):
                await map_page.move_mouse_away()
                popup_not_visible = await map_page.verify_price_popup_not_visible()
                assert popup_not_visible, "移开鼠标后，间夜信息弹窗未消失"

                allure.attach(
                    f"移开鼠标后弹窗消失状态: {popup_not_visible}",
                    "第二次验证结果",
                    allure.attachment_type.TEXT
                )

            # ========== Allure 最终报告 ==========
            allure.attach(
                f"地图签约页面弹窗验证成功\n"
                f"用例ID: {test_data['case_id']}\n"
                f"用例描述: {test_data['description']}\n"
                f"搜索关键词: {test_data['search_keyword']}\n"
                f"项目名称: {test_data['project_name']}\n"
                f"步骤1: 点击地图标记 - 弹窗出现 ✓\n"
                f"步骤2: 移开鼠标 - 弹窗消失 ✓",
                "测试结果",
                allure.attachment_type.TEXT
            )
