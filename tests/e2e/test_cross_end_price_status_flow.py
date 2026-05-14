"""
E2E 测试：平台和酒店端的价格状态流转
测试场景: Operate → Hotel → Operate 三阶段串联完整流程
"""
import pytest
import allure
from pages.operate.rfp_management.rfp_contracting_map_page import RFPContractingMapPage
from pages.hotel.contracting.hotel_bidding_page import HotelContractingPage
from utils.config import config
from utils.logger import get_logger
from utils.test_data_loader import TestDataLoader
from utils.excel_utils import generate_signing_status_excel
from utils.timeout_config import timeout_config

logger = get_logger("tests.e2e.test_price_status_flow", config.log_level)

# 加载 E2E 价格状态流转测试数据
E2E_CASES = TestDataLoader.load_params(
    "rfp_management_params.json",
    "e2e_price_status_flow",
)


@allure.feature("E2E 价格状态流转")
@allure.story("平台和酒店端的价格状态流转")
class TestPriceStatusFlow:
    """平台和酒店端的价格状态流转测试"""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "case_data",
        E2E_CASES,
        ids=[case["case_id"] for case in E2E_CASES],
    )
    @allure.title("验证 Operate → Hotel → Operate 完整价格状态流转")
    @allure.description("""
    测试: 平台端（Operate）设置酒店为议价中状态，
    酒店端（Hotel）提交修改报价，
    最后平台端验证酒店变为修订报价并执行中签操作。

    测试流程:
    Phase 1 - Operate: 去签约 → 导入议价中状态
    Phase 2 - Hotel: 修改报价 → 提交报价 → 断言成功
    Phase 3 - Operate: 修订报价页签验证 → 中签操作 → 断言中签
    """)
    async def test_price_status_flow(
        self,
        operate_e2e_login,
        hotel_e2e_login,
        case_data: dict,
    ):
        """完整价格状态流转测试"""
        project_name = case_data["project_name"]
        hotel_name = case_data["hotel_name"]
        hotel_id = case_data["hotel_id"]
        import_status = case_data["import_status"]
        case_id = case_data["case_id"]
        phase3_initial_tab = case_data["phase3_initial_tab"]
        action = case_data["action"]
        phase3_target_tab = case_data["phase3_target_tab"]
        message = case_data["message"]

        logger.info(
            f"开始 E2E 价格状态流转测试, case: {case_id}, "
            f"project: {project_name}, hotel: {hotel_name}"
        )

        operate_page = operate_e2e_login
        hotel_page = hotel_e2e_login
        map_page = RFPContractingMapPage(operate_page)
        hotel_page_object = HotelContractingPage(hotel_page)

        # ======================================================================
        # Phase 1: Operate 端 - 去签约并导入酒店状态为议价中
        # ======================================================================

        with allure.step("【Phase 1】Operate 端操作"):
            with allure.step("进入 /home 页面"):
                await map_page.navigate_to_home()

            with allure.step("通过菜单进入签约页面"):
                await map_page.navigate_to_contracting()

            with allure.step("选择 Started Tab"):
                await map_page.click_started_tab()

            with allure.step(f"搜索项目: {project_name}"):
                await map_page.search_project_by_keyword(project_name)

            with allure.step("点击首个去签约按钮"):
                await map_page.click_contract_signing()

            # 生成并导入签约状态 Excel
            excel_file_name = f"RFP_import_signing_status_{case_id}.xlsx"
            excel_path = generate_signing_status_excel(
                header=["HotelId", "Contract Status", "Remark"],
                data_rows=[[hotel_id, import_status, ""]],
                file_name=excel_file_name,
            )
            allure.attach(
                f"酒店ID: {hotel_id}, 导入状态: {import_status}",
                "签约状态导入文件内容",
                allure.attachment_type.TEXT,
            )

            with allure.step("切换到列表模式"):
                await map_page.switch_to_list_mode()

            with allure.step(f"导入签约状态: {import_status}"):
                await map_page.import_signing_status_file(excel_path)

            with allure.step("等待导入签约完成"):
                await operate_page.wait_for_timeout(
                    timeout_config.get_quick_step_timeout()
                )

            with allure.step("切换回地图模式"):
                await map_page.switch_to_map_mode()

        # ======================================================================
        # Phase 2: Hotel 端 - 修改报价并提交
        # ======================================================================

        with allure.step("【Phase 2】Hotel 端操作"):
            with allure.step("进入 /home 页面"):
                await hotel_page_object.navigate_to_home()

            with allure.step("通过菜单进入签约页面"):
                await hotel_page_object.navigate_to_contracting()

            with allure.step("选择 Rebid Tab（模糊匹配数字后缀）"):
                await hotel_page_object.select_rebid_tab()

            with allure.step(f"搜索项目: {project_name}"):
                await hotel_page_object.search_project(project_name)

            with allure.step(f"搜索酒店并选择: {hotel_name}"):
                await hotel_page_object.search_hotel_and_select(hotel_name)

            with allure.step("点击搜索按钮"):
                await hotel_page_object.click_search()

            with allure.step(f"点击 Modify Proposal"):
                await hotel_page_object.click_modify_proposal_for_project(
                    project_name
                )

            with allure.step("点击 Submit quotation"):
                await hotel_page_object.click_submit_quotation()

            with allure.step("点击确认弹窗 OK"):
                await hotel_page_object.click_confirm_ok()

            with allure.step("断言操作成功 toast"):
                success = await hotel_page_object.wait_for_success_toast()
                assert success, (
                    "Hotel 端提交报价后未检测到成功提示 Toast"
                )

        # ======================================================================
        # Phase 3: Operate 端 - 验证修订报价并执行中签
        # ======================================================================

        with allure.step("【Phase 3】Operate 端中签操作"):
            with allure.step(f"点击 {phase3_initial_tab} 价格页签"):
                await map_page.click_price_status_tab(phase3_initial_tab)

            with allure.step(f"验证 {phase3_initial_tab} 页签下存在酒店"):
                hotel_exists = await map_page.verify_hotel_exists()
                assert hotel_exists, (
                    f"{phase3_initial_tab} 页签下未找到酒店，"
                    "酒店可能未成功提交修改报价"
                )

            with allure.step("点击首个酒店"):
                await map_page.click_first_hotel()

            with allure.step(f"执行操作 ({action})"):
                await map_page.click_action_by_type(action)

            with allure.step("输入留言"):
                await map_page.fill_message(message)

            with allure.step("点击确定"):
                await map_page.click_confirm()

            with allure.step(f"点击 {phase3_target_tab} 价格页签"):
                await map_page.click_price_status_tab(phase3_target_tab)

            with allure.step(f"验证 {phase3_target_tab} 页签下存在酒店"):
                accepted_exists = await map_page.verify_hotel_exists()
                assert accepted_exists, (
                    f"{phase3_target_tab} 页签下未找到酒店，中签操作可能未生效"
                )

        # ======================================================================
        # 测试结果报告
        # ======================================================================
        result_report = f"""
        [OK] E2E 价格状态流转测试完成

        【测试用例】
        - case_id: {case_id}
        - description: {case_data['description']}
        - 项目名称: {project_name}
        - 酒店名称: {hotel_name}
        - 酒店 ID: {hotel_id}

        【流转流程】
        Phase 1 - Operate: 导入状态 → {import_status}
        Phase 2 - Hotel: 修改报价 → 提交报价 → Toast 成功 ✓
        Phase 3 - Operate: {phase3_initial_tab} 页签验证 ✓ → {action} → {phase3_target_tab} 页签验证 ✓

        【测试状态】 通过
        """
        allure.attach(
            result_report, "测试结果", allure.attachment_type.TEXT
        )

        logger.info(f"E2E 价格状态流转测试通过: {case_id}")