"""
酒店端报价管理 Page Object Model
负责酒店端在 Contracting 页面中的报价操作交互
"""

from playwright.async_api import Page
from pages.common.base_page import BasePage
from utils.config import config
from utils.timeout_config import timeout_config
from utils.logger import get_logger
import allure
import re


class HotelContractingPage(BasePage):
    """酒店端 Contracting 报价管理 Page Object"""

    # ========== 导航菜单 ==========
    WORK_TABLE_BUTTON_NAME = "Work Table"
    WORK_TABLE_MENUITEM_NAME = "Work table"
    RFP_MANAGEMENT_BUTTON_NAME = "RFP Management"
    CONTRACTING_MENUITEM_NAME = "Contracting"

    # ========== Tab ==========
    # Rebid 标签页，后面带数字后缀，如 "Rebid (16)"，需要模糊匹配
    REBID_TAB_PATTERN = r"^Rebid"

    # ========== 搜索框 ==========
    PROJECT_SEARCH_PATTERN = r"^Project$"
    HOTEL_NAME_SEARCH_PATTERN = r"^Hotel Name$"
    SEARCH_BUTTON_SELECTOR = "button.el-button--primary.is-circle"
    SEARCH_FILTER_NTH = 1

    # ========== 操作按钮 ==========
    MODIFY_PROPOSAL_TEXT = "Modify Proposal"
    SUBMIT_QUOTATION_BUTTON_TEXT = "Submit quotation"
    CONFIRM_OK_BUTTON_TEXT = "OK"

    # ========== Toast 断言 ==========
    SUCCESS_TOAST_SELECTOR = "div.el-message--success"

    def __init__(self, page: Page):
        super().__init__(page)
        self.logger = get_logger(self.__class__.__name__, config.log_level)

    # ========== 导航 ==========

    async def navigate_to_home(self) -> None:
        """进入 /home 页面"""
        self.logger.info("开始进入 /home 页面")
        with allure.step("进入 /home 页面"):
            home_url = f"{config.base_url.rstrip('/')}/home"
            await self.page.goto(home_url, wait_until="domcontentloaded")
            await self.wait_helper.wait_for_url(
                self.page, "**/home*", timeout=timeout_config.get_navigation_timeout()
            )
            self.logger.info("[OK] 已进入 /home 页面")

    async def navigate_to_contracting(self) -> None:
        """通过菜单导航至 Contracting 页面"""
        self.logger.info("开始导航至 Contracting 页面")

        with allure.step("导航至 Contracting 页面"):
            try:
                # Step 1: 点击 Work Table 菜单
                self.logger.debug("点击 Work Table 菜单")
                work_table_btn = self.page.get_by_role("button", name=self.WORK_TABLE_BUTTON_NAME)
                await work_table_btn.click()
                self.logger.info("Work Table 菜单已点击")

                # Step 2: 点击 Work table 子菜单
                self.logger.debug("点击 Work table 子菜单")
                work_table_item = self.page.get_by_role("menuitem", name=self.WORK_TABLE_MENUITEM_NAME)
                await work_table_item.click()
                self.logger.info("Work table 子菜单已点击")

                # Step 3: 点击 RFP Management 菜单
                self.logger.debug("点击 RFP Management 菜单")
                rfp_menu = self.page.get_by_role("button", name=self.RFP_MANAGEMENT_BUTTON_NAME)
                await rfp_menu.click()
                self.logger.info("RFP Management 菜单已点击")

                # Step 4: 点击 Contracting 子菜单
                self.logger.debug("点击 Contracting 子菜单")
                contracting_item = self.page.get_by_role("menuitem", name=self.CONTRACTING_MENUITEM_NAME)
                await contracting_item.click()
                self.logger.info("Contracting 子菜单已点击")

                # Step 5: 等待页面加载
                await self.page.wait_for_load_state("networkidle")
                allure.attach("Contracting 页面已加载", "导航结果")
                self.logger.info("Contracting 页面加载完成")

            except Exception as e:
                error_msg = f"导航至 Contracting 页面失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "导航错误")
                raise

    # ========== Tab 选择 ==========

    async def select_rebid_tab(self) -> None:
        """选择 Rebid 标签页（模糊匹配数字后缀，如 Rebid (16)）"""
        self.logger.info("开始选择 Rebid Tab")

        with allure.step("选择 Rebid Tab"):
            try:
                rebid_tab = self.page.get_by_role("tab").filter(
                    has_text=re.compile(self.REBID_TAB_PATTERN)
                )
                await rebid_tab.wait_for(timeout=timeout_config.get_element_timeout())
                await rebid_tab.click()
                await self.page.wait_for_load_state("networkidle")
                self.logger.info("[OK] Rebid Tab 已选择")
            except Exception as e:
                error_msg = f"选择 Rebid Tab 失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "Tab 选择错误")
                raise

    # ========== 搜索 ==========

    async def search_project(self, keyword: str) -> None:
        """在搜索栏输入项目名称

        Args:
            keyword: 项目名称关键词
        """
        self.logger.info(f"搜索项目: {keyword}")

        with allure.step(f"搜索项目: {keyword}"):
            try:
                project_filter = self.page.locator("div").filter(
                    has_text=re.compile(self.PROJECT_SEARCH_PATTERN)
                ).nth(self.SEARCH_FILTER_NTH)
                await project_filter.click()
                await self.page.wait_for_timeout(300)

                search_input = project_filter.locator("input.el-input__inner")
                await search_input.clear()
                await search_input.fill(keyword)
                self.logger.info(f"项目关键词已输入: {keyword}")
            except Exception as e:
                error_msg = f"搜索项目失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "搜索错误")
                raise

    async def search_hotel_and_select(self, hotel_name: str) -> None:
        """输入酒店名称并从下拉框选择

        Args:
            hotel_name: 酒店名称
        """
        self.logger.info(f"搜索酒店: {hotel_name}")

        with allure.step(f"搜索酒店: {hotel_name}"):
            try:
                # Step 1: 点击 Hotel Name 搜索框
                hotel_filter = self.page.locator("div").filter(
                    has_text=re.compile(self.HOTEL_NAME_SEARCH_PATTERN)
                ).nth(self.SEARCH_FILTER_NTH)
                await hotel_filter.click()
                await self.page.wait_for_timeout(300)

                # Step 2: 输入酒店名称（限定在 hotel_filter 内，避免误填到项目搜索框）
                search_input = hotel_filter.locator("input.el-select__input")
                await search_input.clear()
                await search_input.fill(hotel_name)
                await self.page.wait_for_timeout(500)

                # Step 3: 从下拉框选择匹配项
                self.logger.debug("从下拉框选择酒店")
                option = self.page.get_by_role("option").filter(
                    has_text=re.compile(re.escape(hotel_name))
                ).first
                await option.wait_for(timeout=timeout_config.get_element_timeout())
                await option.click()
                self.logger.info(f"酒店已选择: {hotel_name}")
            except Exception as e:
                error_msg = f"搜索酒店失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "酒店搜索错误")
                raise

    async def click_search(self) -> None:
        """点击搜索按钮"""
        self.logger.info("点击搜索按钮")

        with allure.step("点击搜索按钮"):
            try:
                search_btn = self.page.locator(self.SEARCH_BUTTON_SELECTOR)
                await search_btn.wait_for(timeout=timeout_config.get_element_timeout())
                await search_btn.click()
                await self.page.wait_for_load_state("networkidle")
                self.logger.info("[OK] 搜索按钮已点击")
            except Exception as e:
                error_msg = f"点击搜索按钮失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "搜索按钮错误")
                raise

    # ========== 报价操作 ==========

    async def click_modify_proposal_for_project(self, project_name: str) -> None:
        """在匹配指定项目名称的行中点击 Modify Proposal

        Args:
            project_name: 用于定位行的项目名称
        """
        self.logger.info(f"点击项目 [{project_name}] 的 Modify Proposal")

        with allure.step(f"点击 Modify Proposal"):
            try:
                # 遍历表格行，找到包含精确项目名称的行
                row = self.page.locator("tr").filter(
                    has_text=re.compile(re.escape(project_name))
                )
                modify_btn = row.get_by_text(self.MODIFY_PROPOSAL_TEXT)
                await modify_btn.wait_for(timeout=timeout_config.get_element_timeout())
                await modify_btn.click()
                await self.page.wait_for_timeout(500)
                self.logger.info(f"[OK] Modify Proposal 已点击")
            except Exception as e:
                error_msg = f"点击 Modify Proposal 失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "Modify Proposal 错误")
                raise

    async def click_submit_quotation(self) -> None:
        """点击提交报价按钮"""
        self.logger.info("点击 Submit quotation 按钮")

        with allure.step("点击 Submit quotation"):
            try:
                submit_btn = self.page.get_by_role(
                    "button", name=self.SUBMIT_QUOTATION_BUTTON_TEXT
                )
                await submit_btn.wait_for(timeout=timeout_config.get_element_timeout())
                await submit_btn.click()
                await self.page.wait_for_timeout(300)
                self.logger.info("[OK] Submit quotation 已点击")
            except Exception as e:
                error_msg = f"点击 Submit quotation 失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "Submit quotation 错误")
                raise

    async def click_confirm_ok(self) -> None:
        """点击二次确认弹窗的 OK 按钮"""
        self.logger.info("点击确认弹窗 OK 按钮")

        with allure.step("点击确认弹窗 OK"):
            try:
                ok_btn = self.page.get_by_role(
                    "button", name=self.CONFIRM_OK_BUTTON_TEXT, exact=True
                )
                await ok_btn.wait_for(timeout=timeout_config.get_element_timeout())
                await ok_btn.click()
                await self.page.wait_for_timeout(500)
                self.logger.info("[OK] 确认 OK 已点击")
            except Exception as e:
                error_msg = f"点击 OK 按钮失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "OK 按钮错误")
                raise

    # ========== 断言 ==========

    async def wait_for_success_toast(self) -> bool:
        """等待操作成功的 toast 出现

        Returns:
            bool: 是否出现成功 toast
        """
        self.logger.info("等待操作成功 toast")

        with allure.step("验证操作成功 toast"):
            try:
                toast = self.page.locator(self.SUCCESS_TOAST_SELECTOR)
                await toast.wait_for(timeout=timeout_config.get_element_timeout())
                is_visible = await toast.is_visible()
                if is_visible:
                    toast_text = await toast.text_content()
                    self.logger.info(f"[OK] 成功 toast 出现: {toast_text}")
                    allure.attach(f"toast 内容: {toast_text}", "操作成功")
                return is_visible
            except Exception as e:
                self.logger.warning(f"未检测到成功 toast: {str(e)}")
                allure.attach("未检测到成功 toast", "断言结果")
                return False

    async def get_current_url(self) -> str:
        """获取当前页面 URL"""
        return self.page.url