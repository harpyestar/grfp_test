"""
RFP 项目报价详情页面对象模型
负责 Contracting 页面详情页中的内部跟进备注功能交互
"""

from playwright.async_api import Page
from pages.common.base_page import BasePage
from utils.config import config
from utils.timeout_config import timeout_config
from utils.logger import get_logger
from datetime import datetime
import allure
import re


class RFPDetailPageProject(BasePage):
    """RFP 项目报价详情页 Page Object"""

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

    # ========== 详情页相关元素 ==========
    DETAIL_BUTTON_TEXT = "Detail"
    INTERNAL_NOTES_BUTTON_NAMES = ["Internal Memo", "内部备注", "内部跟进备注"]
    NOTES_INPUT_PLACEHOLDERS = ["请输入内部跟进备注", "请输入内部备注"]
    NOTES_TEXTAREA_SELECTOR = ".el-dialog__body textarea.el-textarea__inner"
    NOTES_CONFIRM_BUTTON_NAMES = ["确定", "Confirm", "Save"]

    def __init__(self, page: Page):
        super().__init__(page)
        self.logger = get_logger(self.__class__.__name__, config.log_level)

    # ========== 辅助方法 ==========
    def _generate_timestamp(self) -> str:
        """生成时间戳格式: YYYYMMDD-HHMMSS"""
        return datetime.now().strftime("%Y%m%d-%H%M%S")

    async def _click_first_visible_button(self, page: Page, button_names: list[str]) -> str:
        """点击首个可见按钮并返回按钮名称"""
        last_error = None

        for button_name in button_names:
            try:
                button = page.get_by_role("button", name=button_name).first
                await button.wait_for(timeout=timeout_config.get_element_timeout())
                if await button.is_visible():
                    await button.click()
                    return button_name
            except Exception as e:
                last_error = e
                self.logger.debug(f"按钮未命中: {button_name}, error: {str(e)}")

        raise RuntimeError(
            f"未找到可点击按钮，候选名称: {button_names}，最后错误: {str(last_error)}"
        )

    async def _fill_first_visible_input(self, page: Page, placeholders: list[str], content: str) -> str:
        """填写首个可见输入框并返回命中的定位说明"""
        last_error = None

        for placeholder in placeholders:
            try:
                input_box = page.get_by_placeholder(placeholder).first
                await input_box.wait_for(timeout=timeout_config.get_element_timeout())
                if await input_box.is_visible():
                    await input_box.click()
                    await input_box.fill(content)
                    return f"placeholder={placeholder}"
            except Exception as e:
                last_error = e
                self.logger.debug(f"输入框未命中: {placeholder}, error: {str(e)}")

        try:
            textarea = page.locator(self.NOTES_TEXTAREA_SELECTOR).first
            await textarea.wait_for(timeout=timeout_config.get_element_timeout())
            if await textarea.is_visible():
                await textarea.click()
                await textarea.fill(content)
                return f"selector={self.NOTES_TEXTAREA_SELECTOR}"
        except Exception as e:
            last_error = e
            self.logger.debug(f"textarea 未命中: {self.NOTES_TEXTAREA_SELECTOR}, error: {str(e)}")

        raise RuntimeError(
            f"未找到可填写输入框，候选占位文本: {placeholders}，"
            f"textarea 选择器: {self.NOTES_TEXTAREA_SELECTOR}，最后错误: {str(last_error)}"
        )

    async def _get_detail_page_text(self, detail_page: Page) -> str:
        """获取详情页文本内容"""
        body = detail_page.locator("body")
        await body.wait_for(timeout=timeout_config.get_element_timeout())
        return await body.inner_text()

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
                self.logger.debug("查找第一个酒店元素 (class='p-4 border-bottom cursor-pointer')")

                # 定位酒店列表项
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

    # ========== 详情页交互方法 ==========
    async def click_detail_button(self):
        """点击 Detail 按钮打开详情页弹窗"""
        self.logger.info("开始点击 Detail 按钮")

        with allure.step("点击 Detail 按钮打开详情页"):
            try:
                self.logger.debug(f"定位 {self.DETAIL_BUTTON_TEXT} 按钮")
                detail_btn = self.page.get_by_role("button", name=self.DETAIL_BUTTON_TEXT)
                await detail_btn.wait_for(timeout=timeout_config.get_element_timeout())

                async with self.page.expect_popup() as popup_info:
                    await detail_btn.click()
                    self.logger.info("Detail 按钮已点击，等待新页面打开")

                detail_page = await popup_info.value
                self.logger.info("详情页新页面已打开")

                await detail_page.wait_for_load_state("domcontentloaded")
                await detail_page.wait_for_load_state("networkidle")
                allure.attach("详情页新页面已打开", "操作结果")

                return detail_page

            except Exception as e:
                error_msg = f"点击 Detail 按钮失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "点击错误")
                raise

    async def click_internal_notes_button(self, detail_page: Page) -> None:
        """在详情页中点击内部跟进备注按钮"""
        self.logger.info("开始点击内部跟进备注按钮")

        with allure.step("点击内部跟进备注按钮"):
            try:
                clicked_button_name = await self._click_first_visible_button(
                    detail_page,
                    self.INTERNAL_NOTES_BUTTON_NAMES,
                )

                await detail_page.wait_for_timeout(300)
                allure.attach(f"已点击备注按钮: {clicked_button_name}", "备注按钮定位")
                self.logger.info(f"备注按钮点击完成: {clicked_button_name}")

            except Exception as e:
                error_msg = f"点击备注按钮失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "点击错误")
                raise

    async def fill_internal_notes(self, detail_page: Page, notes_content: str = None) -> str:
        """填写内部跟进备注内容"""
        self.logger.info("开始填写内部跟进备注")

        with allure.step("填写备注内容"):
            try:
                if notes_content is None:
                    timestamp = self._generate_timestamp()
                    notes_content = f"hy-自动化书写文字-{timestamp}"

                self.logger.debug(f"备注内容: {notes_content}")

                matched_placeholder = await self._fill_first_visible_input(
                    detail_page,
                    self.NOTES_INPUT_PLACEHOLDERS,
                    notes_content,
                )

                allure.attach(
                    f"备注内容: {notes_content}\n命中占位文本: {matched_placeholder}",
                    "备注填充"
                )
                self.logger.info(f"备注内容填充完成: {notes_content}")

                return notes_content

            except Exception as e:
                error_msg = f"填写备注失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "填充错误")
                raise

    async def click_notes_confirm_button(self, detail_page: Page) -> None:
        """点击备注确定按钮保存备注"""
        self.logger.info("开始点击备注确定按钮")

        with allure.step("点击确定按钮保存备注"):
            try:
                clicked_button_name = await self._click_first_visible_button(
                    detail_page,
                    self.NOTES_CONFIRM_BUTTON_NAMES,
                )

                await detail_page.wait_for_timeout(500)
                allure.attach(f"已点击确定按钮: {clicked_button_name}", "确定按钮定位")
                self.logger.info(f"备注确定按钮点击完成: {clicked_button_name}")

            except Exception as e:
                error_msg = f"点击确定按钮失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "点击错误")
                raise

    async def refresh_detail_page(self, detail_page: Page) -> None:
        """刷新详情页"""
        self.logger.info("开始刷新详情页")

        with allure.step("刷新详情页"):
            try:
                # 刷新页面
                await detail_page.reload(wait_until="networkidle")
                self.logger.info("详情页已刷新")

                # 等待页面加载完成
                await detail_page.wait_for_load_state("networkidle")
                allure.attach("详情页已刷新并加载完成", "刷新结果")
                self.logger.info("详情页刷新完成")

            except Exception as e:
                error_msg = f"刷新详情页失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "刷新错误")
                raise

    async def verify_notes_in_detail_page(self, detail_page: Page, expected_notes: str) -> bool:
        """验证备注内容是否在详情页中显示"""
        self.logger.info(f"开始验证备注内容: {expected_notes}")

        with allure.step(f"验证备注内容是否显示: {expected_notes}"):
            try:
                page_text = await self._get_detail_page_text(detail_page)
                is_visible = expected_notes in page_text

                allure.attach(
                    f"期望备注: {expected_notes}\n"
                    f"验证结果: {is_visible}",
                    "备注验证"
                )

                self.logger.info(f"备注验证完成: {is_visible}")
                return is_visible

            except Exception as e:
                error_msg = f"验证备注失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "验证错误")
                return False

    async def close_detail_page(self, detail_page: Page) -> None:
        """关闭详情页新页面"""
        self.logger.info("开始关闭详情页新页面")

        with allure.step("关闭详情页新页面"):
            try:
                if detail_page.is_closed():
                    self.logger.info("详情页新页面已关闭，跳过关闭操作")
                    return

                await detail_page.close()
                self.logger.info("详情页新页面已关闭")

                allure.attach("详情页新页面已关闭", "关闭结果")
                self.logger.info("新页面关闭完成")


            except Exception as e:
                error_msg = f"关闭详情页失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "关闭错误")
                raise