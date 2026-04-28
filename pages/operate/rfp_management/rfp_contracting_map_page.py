"""
RFP 项目地图签约页面对象模型
负责 Contracting 页面地图模式下的酒店标记交互和间夜信息验证
"""

from playwright.async_api import Page
from pages.common.base_page import BasePage
from utils.config import config
from utils.timeout_config import timeout_config
from utils.logger import get_logger
import allure
import re


class RFPContractingMapPage(BasePage):
    """RFP 项目地图签约 Page Object"""

    # ========== 导航菜单元素 ==========
    RFP_MANAGEMENT_MENU_NAME = "RFP Management"
    CONTRACTING_MENU_TEXT = "Contracting"

    # ========== Contracting 标签页 ==========
    STARTED_TAB_NAME = "Started"

    # ========== 搜索框元素 ==========
    PROJECT_SEARCH_FILTER_PATTERN = r"^Project$"
    PROJECT_SEARCH_FILTER_NTH = 1
    SEARCH_BUTTON_SELECTOR = ".search > .btn"

    # ========== Contract Signing 按钮 ==========
    CONTRACT_SIGNING_BUTTON_TEXT = "Contract Signing"

    # ========== 新标的页签 ==========
    NEW_PROPOSAL_TAB_NAME = "New proposal"

    # ========== 地图相关元素 ==========
    # 地图上的酒店标记（使用 getByLabel + getByText）
    MAP_MARKER_LABEL = "Map marker"
    MAP_MARKER_TEXT = "New proposal"

    # 间夜信息弹窗（price-popup）
    PRICE_POPUP_SELECTOR = ".price-popup"
    PRICE_VALUE_SELECTOR = ".price-value"
    PRICE_POPUP_FULL_SELECTOR = ".price-popup .price-value"

    def __init__(self, page: Page):
        super().__init__(page)
        self.logger = get_logger(self.__class__.__name__, config.log_level)

    # ========== 导航方法 ==========
    async def navigate_to_contracting(self) -> None:
        """导航至 Contracting 页面"""
        self.logger.info("开始导航至 Contracting 页面")

        with allure.step("导航至 Contracting 页面"):
            try:
                # Step 1: 点击 RFP Management 菜单
                self.logger.debug("点击 RFP Management 菜单")
                rfp_menu = self.page.get_by_role("button", name=self.RFP_MANAGEMENT_MENU_NAME)
                await rfp_menu.click()
                self.logger.info("RFP Management 菜单已点击")

                # Step 2: 等待下拉菜单
                await self.page.wait_for_timeout(300)

                # Step 3: 点击 Contracting 菜单项
                self.logger.debug(f"点击 {self.CONTRACTING_MENU_TEXT} 菜单项")
                contracting_menu = self.page.get_by_label(self.RFP_MANAGEMENT_MENU_NAME).get_by_text(
                    self.CONTRACTING_MENU_TEXT
                )
                await contracting_menu.click()
                self.logger.info("Contracting 菜单项已点击")

                # Step 4: 等待页面加载
                await self.page.wait_for_load_state("networkidle")
                allure.attach("Contracting 页面已加载", "导航结果")
                self.logger.info("Contracting 页面加载完成")

            except Exception as e:
                error_msg = f"导航至 Contracting 页面失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "导航错误")
                raise

    async def click_started_tab(self) -> None:
        """点击 Started Tab"""
        self.logger.info("开始点击 Started Tab")

        with allure.step(f"选择 {self.STARTED_TAB_NAME} Tab"):
            try:
                # 点击 Started Tab
                self.logger.debug(f"定位 {self.STARTED_TAB_NAME} Tab")
                started_tab = self.page.get_by_role("tab", name=self.STARTED_TAB_NAME, exact=True)
                await started_tab.click()
                self.logger.info("Started Tab 已点击")

                # 等待表格加载
                await self.page.wait_for_load_state("networkidle")
                allure.attach(f"已选择: {self.STARTED_TAB_NAME}", "Tab 选择")
                self.logger.info(f"{self.STARTED_TAB_NAME} Tab 加载完成")

            except Exception as e:
                error_msg = f"点击 Started Tab 失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "点击错误")
                raise

    async def search_project_by_keyword(self, keyword: str) -> None:
        """通过关键词搜索项目"""
        self.logger.info(f"开始搜索项目: {keyword}")

        with allure.step(f"搜索项目关键词: {keyword}"):
            try:
                # Step 1: 点击 Project 搜索框
                self.logger.debug("定位 Project 搜索框")
                project_filter = self.page.locator("div").filter(
                    has_text=re.compile(self.PROJECT_SEARCH_FILTER_PATTERN)
                ).nth(self.PROJECT_SEARCH_FILTER_NTH)
                await project_filter.click()
                self.logger.info("Project 搜索框已点击")

                # Step 2: 等待并输入关键词
                await self.page.wait_for_timeout(300)
                self.logger.debug(f"输入搜索关键词: {keyword}")
                search_input = project_filter.locator("input.el-input__inner")
                await search_input.clear()
                await search_input.fill(keyword)
                await self.page.wait_for_timeout(200)
                self.logger.info(f"搜索关键词已输入: {keyword}")

                # Step 3: 点击搜索按钮
                self.logger.debug("点击搜索按钮")
                search_btn = self.page.locator(self.SEARCH_BUTTON_SELECTOR)
                await search_btn.click()
                self.logger.info("搜索按钮已点击")

                # Step 4: 等待搜索结果加载
                await self.page.wait_for_load_state("networkidle")
                allure.attach(f"搜索关键词: {keyword}", "搜索操作")
                self.logger.info("[OK] 项目搜索完成")

            except Exception as e:
                error_msg = f"搜索项目失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "搜索错误")
                raise

    async def click_contract_signing(self) -> None:
        """点击第一个 Contract Signing 按钮"""
        self.logger.info("开始点击 Contract Signing 按钮")

        with allure.step("点击 Contract Signing 按钮"):
            try:
                # 找到第一个 Contract Signing 按钮并点击
                self.logger.debug(f"定位 {self.CONTRACT_SIGNING_BUTTON_TEXT} 按钮")
                contract_signing_btn = self.page.get_by_text(self.CONTRACT_SIGNING_BUTTON_TEXT).first
                await contract_signing_btn.click()
                self.logger.info("Contract Signing 按钮已点击")

                # 等待签约页面加载
                await self.page.wait_for_load_state("networkidle")
                allure.attach("Contract Signing 页面已打开", "操作结果")
                self.logger.info("Contract Signing 页面加载完成")

            except Exception as e:
                error_msg = f"点击 Contract Signing 失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "点击错误")
                raise

    async def click_new_proposal_tab(self) -> None:
        """点击 New proposal 标签页"""
        self.logger.info("开始点击 New proposal 标签页")

        with allure.step(f"选择 {self.NEW_PROPOSAL_TAB_NAME} 标签页"):
            try:
                # 点击 New proposal 标签页
                self.logger.debug(f"定位 {self.NEW_PROPOSAL_TAB_NAME} 标签页")
                new_proposal_btn = self.page.get_by_role("button", name=self.NEW_PROPOSAL_TAB_NAME)
                await new_proposal_btn.click()
                self.logger.info("New proposal 标签页已点击")

                # 等待页面加载
                await self.page.wait_for_load_state("networkidle")
                allure.attach(f"已选择: {self.NEW_PROPOSAL_TAB_NAME}", "标签页选择")
                self.logger.info(f"{self.NEW_PROPOSAL_TAB_NAME} 标签页加载完成")

            except Exception as e:
                error_msg = f"点击 New proposal 标签页失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "点击错误")
                raise

    async def select_first_hotel(self) -> None:
        """在 New proposal 标签页中选择第一个酒店"""
        self.logger.info("开始选择第一个酒店")

        with allure.step("选择第一个酒店"):
            try:
                # 根据提供的 HTML 结构，酒店列表项具有特定的 class 组合：
                # class="p-4 border-bottom cursor-pointer active"
                # 使用精确的 class 选择器定位
                self.logger.debug("查找第一个酒店元素 (class='p-4 border-bottom cursor-pointer')")

                # 定位酒店列表项：使用复合选择器
                hotel_item_selector = "div.p-4.border-bottom.cursor-pointer"
                first_hotel = self.page.locator(hotel_item_selector).first

                # 等待元素可见
                await first_hotel.wait_for(timeout=timeout_config.get_element_timeout())
                self.logger.debug("第一个酒店元素已找到，准备点击")

                # 点击酒店
                await first_hotel.click()
                self.logger.info("第一个酒店已选中")

                # 等待页面反应
                await self.page.wait_for_timeout(500)
                allure.attach("第一个酒店已选择", "酒店选择")
                self.logger.info("酒店选择完成")

            except Exception as e:
                error_msg = f"选择酒店失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "选择错误")
                raise

    # ========== 地图交互方法 ==========
    async def hover_map_marker(self) -> None:
        """模拟鼠标悬浮到地图标记"""
        self.logger.info("开始悬浮到地图标记")

        with allure.step("悬浮到地图标记"):
            try:
                # 定位地图上的标记（使用 getByLabel + getByText）
                self.logger.debug(f"定位地图标记: {self.MAP_MARKER_LABEL} - {self.MAP_MARKER_TEXT}")
                map_marker = self.page.get_by_label(self.MAP_MARKER_LABEL).get_by_text(self.MAP_MARKER_TEXT)

                # 等待标记可见
                await map_marker.wait_for(timeout=timeout_config.get_element_timeout())

                # 悬浮鼠标
                await map_marker.hover()
                self.logger.info("鼠标已悬浮到标记上")

                # 等待弹窗可能出现
                await self.page.wait_for_timeout(300)
                allure.attach("鼠标已悬浮", "交互操作")
                self.logger.info("悬浮操作完成")

            except Exception as e:
                error_msg = f"悬浮地图标记失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "悬浮错误")
                raise

    async def click_map_marker(self) -> None:
        """点击地图标记"""
        self.logger.info("开始点击地图标记")

        with allure.step("点击地图标记"):
            try:
                # 定位地图上的标记
                self.logger.debug(f"定位地图标记: {self.MAP_MARKER_LABEL} - {self.MAP_MARKER_TEXT}")
                map_marker = self.page.get_by_label(self.MAP_MARKER_LABEL).get_by_text(self.MAP_MARKER_TEXT)

                # 等待标记可见
                await map_marker.wait_for(timeout=timeout_config.get_element_timeout())

                # 点击标记
                # 循环点击2次把
                for _ in range(3):
                    await map_marker.click()
                self.logger.info("地图标记已点击")

                # 等待弹窗出现
                await self.page.wait_for_timeout(300)
                allure.attach("地图标记已点击", "交互操作")
                self.logger.info("点击操作完成")

            except Exception as e:
                error_msg = f"点击地图标记失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "点击错误")
                raise

    async def move_mouse_away(self) -> None:
        """将鼠标移开（移动到页面其他位置）"""
        self.logger.info("开始将鼠标移开")

        with allure.step("将鼠标移开"):
            try:
                # 获取页面中心坐标，然后移动鼠标到另一个位置
                self.logger.debug("获取页面尺寸")
                viewport_size = self.page.viewport_size

                if viewport_size:
                    # 移动鼠标到页面左上角
                    move_x = 100
                    move_y = 100
                    self.logger.debug(f"移动鼠标到 ({move_x}, {move_y})")
                    await self.page.mouse.move(move_x, move_y)

                # 等待弹窗可能消失
                await self.page.wait_for_timeout(300)
                allure.attach("鼠标已移开", "交互操作")
                self.logger.info("鼠标移开完成")

            except Exception as e:
                error_msg = f"移开鼠标失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "移开错误")
                raise

    # ========== 弹窗验证方法 ==========
    async def verify_price_popup_visible(self) -> bool:
        """验证间夜信息弹窗是否可见"""
        self.logger.info("开始验证间夜信息弹窗可见性")

        with allure.step("验证弹窗是否可见"):
            try:
                # 定位弹窗（通过完整选择器）
                self.logger.debug(f"定位价格弹窗: {self.PRICE_POPUP_SELECTOR}")
                popup = self.page.locator(self.PRICE_POPUP_SELECTOR)

                # 检查弹窗是否可见
                is_visible = await popup.is_visible()
                self.logger.info(f"弹窗可见性: {is_visible}")

                if is_visible:
                    # 获取弹窗内容
                    price_value = await self.page.locator(self.PRICE_POPUP_FULL_SELECTOR).text_content()
                    self.logger.debug(f"弹窗内容: {price_value}")
                    allure.attach(f"弹窗已出现\n内容: {price_value}", "验证结果")
                else:
                    allure.attach("弹窗未出现", "验证结果")

                self.logger.info(f"弹窗可见性验证完成: {is_visible}")
                return is_visible

            except Exception as e:
                error_msg = f"验证弹窗可见性失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "验证错误")
                return False

    async def verify_price_popup_not_visible(self) -> bool:
        """验证间夜信息弹窗不可见"""
        self.logger.info("开始验证间夜信息弹窗不可见")

        with allure.step("验证弹窗是否不可见"):
            try:
                # 定位弹窗
                self.logger.debug(f"定位价格弹窗: {self.PRICE_POPUP_SELECTOR}")
                popup = self.page.locator(self.PRICE_POPUP_SELECTOR)

                # 检查弹窗是否不可见
                is_visible = await popup.is_visible()
                is_not_visible = not is_visible
                self.logger.info(f"弹窗不可见: {is_not_visible}")

                allure.attach(f"弹窗不可见: {is_not_visible}", "验证结果")
                self.logger.info(f"弹窗不可见验证完成: {is_not_visible}")
                return is_not_visible

            except Exception as e:
                error_msg = f"验证弹窗不可见失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "验证错误")
                return False
