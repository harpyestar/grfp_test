"""
创建新 RFP 项目页面对象模型
负责 RFP 项目创建流程的所有交互操作
所有超时值从 timeout_config 中读取，所有选择器统一在类变量中定义
"""

from playwright.async_api import Page
from pages.common.base_page import BasePage
from utils.config import config
from utils.timeout_config import timeout_config
from utils.logger import get_logger
from datetime import datetime
import random
import allure


class CreateNewRFPProjectPage(BasePage):
    """创建新 RFP 项目 Page Object"""

    # ========== 导航菜单元素 ==========
    RFP_MANAGEMENT_MENU = "text=RFP Management"
    CREATE_NEW_RFP_PROJECT_MENU = "text=Create new RFP project"
    ORG_NAME_LABEL_WAIT = "Organization Name"  # 用于 wait_for 的 label 文本

    # ========== 表单输入框（使用 getByLabel 定位） ==========
    # 组织名称输入框
    ORGANIZATION_NAME_LABEL = "Organization Name"
    # 项目名称输入框
    PROJECT_NAME_LABEL = "Project name"
    # 联系人输入框
    CONTACT_PERSON_LABEL = "Contact Person"
    # 区号输入框（使用 placeholder）
    AREA_CODE_PLACEHOLDER = "Area Code"
    # 预期合同酒店数量（使用 label）
    EXPECTED_HOTELS_COUNT_LABEL = "Expected number of contracted hotels"

    # ========== 单选框元素（通过 label 文本定位） ==========
    # 签约方式 label 及其 Private RFP 选项
    METHOD_OF_SIGNING_LABEL = "Method of Signing"
    PRIVATE_RFP_VALUE = "2"

    # 通知方式 label 及其 Manual Notification 选项
    NOTIFICATION_METHOD_LABEL = "Signing Status Notification"
    MANUAL_NOTIFICATION_VALUE = "0"

    # 报价报告设置 labels 及其 NO NEED 选项
    GROUP_QUOTATION_LABEL = "GROUP QUOTATION STATUS REPORT"
    GROUP_QUOTATION_VALUE = "0"

    ENTERPRISE_QUOTATION_LABEL = "Enterprise Quotation Status Report"
    ENTERPRISE_QUOTATION_VALUE = "0"

    # ========== 日期选择器 ==========
    # 所有日期选择器共用 placeholder，通过索引区分（3个范围，每个范围2个字段）
    DATE_PICKER_PLACEHOLDER = "Please select"
    # 日期范围索引
    BIDDING_DATE_START_IDX = 0
    BIDDING_DATE_END_IDX = 1
    REGISTRATION_START_IDX = 2
    REGISTRATION_END_IDX = 3
    FIRST_ROUND_START_IDX = 4
    FIRST_ROUND_END_IDX = 5

    # ========== 电话号码输入框 ==========
    # 所有 "Please enter" placeholder 共用，通过索引区分
    PHONE_PLACEHOLDER = "Please enter"
    PHONE_INPUT_IDX = 0  # 电话号码是第一个 "Please enter" 框

    # ========== 自动完成下拉菜单 ==========
    AUTOCOMPLETE_ITEM_SELECTOR = ".el-select-dropdown__item"

    # ========== 提交和结果 ==========
    SAVE_BUTTON_NAME = "Save"
    SUCCESS_MESSAGE_SELECTOR = ".el-message__content"

    # ========== 单选框调试定位器 ==========
    # 用于调试所有 radio 按钮
    ALL_RADIOS_SELECTOR = "input[type='radio']"
    METHOD_LABELS_SELECTOR = "label:has-text('Method')"

    def __init__(self, page: Page):
        super().__init__(page)
        self.logger = get_logger(self.__class__.__name__, config.log_level)

    # ========== 辅助方法 ==========
    def _generate_timestamp(self) -> str:
        """生成时间戳格式: YYYYMMDD-HHMMSS"""
        return datetime.now().strftime("%Y%m%d-%H%M%S")

    def _generate_random_hotels_count(self) -> int:
        """生成随机酒店数量: 1-50"""
        return random.randint(1, 50)

    # ========== 导航方法 ==========
    async def navigate_to_create_rfp(self) -> None:
        """导航至创建新 RFP 项目页面"""
        self.logger.info("开始导航至创建新 RFP 项目页面")

        with allure.step("导航至 RFP Management > Create new RFP project"):
            try:
                # 1. 点击 RFP Management 菜单
                self.logger.debug(f"点击 RFP Management 菜单: {self.RFP_MANAGEMENT_MENU}")
                rfp_menu = await self.find_element(self.RFP_MANAGEMENT_MENU)
                await rfp_menu.click()
                self.logger.info("RFP Management 菜单已点击")

                # 2. 等待下拉菜单出现
                self.logger.debug("等待下拉菜单出现")
                await self.wait_helper.wait_for_selector(
                    self.page,
                    self.CREATE_NEW_RFP_PROJECT_MENU,
                    timeout=timeout_config.get_element_timeout()
                )
                self.logger.info("下拉菜单已出现")

                # 3. 点击 Create new RFP project
                self.logger.debug(f"点击 Create new RFP project: {self.CREATE_NEW_RFP_PROJECT_MENU}")
                create_menu = await self.find_element(self.CREATE_NEW_RFP_PROJECT_MENU)
                await create_menu.click()
                self.logger.info("Create new RFP project 菜单项已点击")

                # 4. 等待表单加载完成（通过等待第一个表单字段）
                self.logger.debug("等待表单字段加载完成")
                org_label_element = self.page.get_by_label(self.ORG_NAME_LABEL_WAIT)
                await org_label_element.wait_for(
                    timeout=timeout_config.get_navigation_timeout()
                )

                allure.attach("导航成功，表单已加载", "导航结果")
                self.logger.info("导航成功，创建新 RFP 项目表单已加载")

            except Exception as e:
                error_msg = f"导航至创建页面失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "导航错误")
                raise

    # ========== 表单填充方法 ==========
    async def fill_organization_name(self, org_name: str = "hyg测试机构") -> None:
        """填写组织名称（自动完成功能：输入后选择匹配的首个选项）"""
        self.logger.info(f"开始填写组织名称: {org_name}")

        with allure.step(f"填写组织名称: {org_name}"):
            try:
                # 使用 getByLabel() - 最稳定的定位方式
                self.logger.debug(f"使用 getByLabel 定位 {self.ORGANIZATION_NAME_LABEL}")
                org_input = self.page.get_by_label(self.ORGANIZATION_NAME_LABEL)

                # 填写组织名称
                await org_input.fill(org_name)
                self.logger.debug(f"已输入组织名称: {org_name}")

                # 等待自动完成选项出现
                await self.page.wait_for_timeout(500)

                # 选择自动完成列表中的第一个选项
                autocomplete_items = await self.page.locator(self.AUTOCOMPLETE_ITEM_SELECTOR).all()
                self.logger.debug(f"找到自动完成选项: {len(autocomplete_items)} 个")

                if autocomplete_items:
                    await autocomplete_items[0].click()
                    self.logger.debug("已选择自动完成的第一个选项")
                    await self.page.wait_for_timeout(300)

                allure.attach(f"组织名称: {org_name}", "填充数据")
                self.logger.info(f"组织名称填写成功: {org_name}")
            except Exception as e:
                error_msg = f"填写组织名称失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "填充错误")
                raise

    async def fill_project_name(self) -> str:
        """填写项目名称（自动生成）"""
        self.logger.info("开始填写项目名称")

        with allure.step("填写项目名称"):
            try:
                timestamp = self._generate_timestamp()
                project_name = f"hyg-自动化项目-{timestamp}"

                # 使用 getByLabel() 定位
                project_input = self.page.get_by_label(self.PROJECT_NAME_LABEL)
                await project_input.fill(project_name)

                allure.attach(f"生成的项目名称: {project_name}", "项目名称")
                self.logger.info(f"项目名称填写成功: {project_name}")
                return project_name
            except Exception as e:
                error_msg = f"填写项目名称失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "填充错误")
                raise

    async def fill_contact_person(self, person: str = "荷叶") -> None:
        """填写联系人"""
        self.logger.info(f"开始填写联系人: {person}")

        with allure.step(f"填写联系人: {person}"):
            try:
                # 使用 getByLabel() 定位
                contact_input = self.page.get_by_label(self.CONTACT_PERSON_LABEL)
                await contact_input.fill(person)
                allure.attach(f"联系人: {person}", "填充数据")
                self.logger.info(f"联系人填写成功: {person}")
            except Exception as e:
                error_msg = f"填写联系人失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "填充错误")
                raise

    async def fill_contact_number(self, area_code: str, phone: str) -> None:
        """填写联系电话（区号 + 电话号码分两个字段）"""
        self.logger.info(f"开始填写联系电话: {area_code} {phone}")

        with allure.step(f"填写联系电话: {area_code} {phone}"):
            try:
                # 填写区号 - 使用 getByPlaceholder()
                self.logger.debug(f"填写区号")
                area_input = self.page.get_by_placeholder(self.AREA_CODE_PLACEHOLDER)
                await area_input.fill(area_code)
                self.logger.debug(f"区号填写成功: {area_code}")

                # 填写电话号码 - 获取所有 "Please enter" 占位符的输入框
                all_please_enter = await self.page.get_by_placeholder(self.PHONE_PLACEHOLDER).all()
                if len(all_please_enter) > self.PHONE_INPUT_IDX:
                    phone_input = all_please_enter[self.PHONE_INPUT_IDX]
                    await phone_input.fill(phone)
                    self.logger.debug(f"电话号码填写成功: {phone}")
                else:
                    self.logger.warning(f"找不到电话号码输入框，期望索引 {self.PHONE_INPUT_IDX}，实际找到 {len(all_please_enter)} 个")
                    raise Exception(f"电话号码输入框不足，期望索引 {self.PHONE_INPUT_IDX}，实际找到 {len(all_please_enter)} 个")

                allure.attach(f"区号: {area_code}, 电话: {phone}", "联系电话")
                self.logger.info(f"联系电话填写成功: {area_code} {phone}")
            except Exception as e:
                error_msg = f"填写联系电话失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "填充错误")
                raise

    # ========== 选择器方法 ==========
    async def select_signing_method(self) -> None:
        """选择签约方式: Private RFP (value=2)"""
        self.logger.info("开始选择签约方式: Private RFP")

        with allure.step("选择签约方式: Private RFP"):
            try:
                # 调试：输出所有radio按钮信息
                self.logger.debug("=== 调试信息：页面上所有单选框 ===")
                all_radios = await self.page.locator(self.ALL_RADIOS_SELECTOR).all()
                self.logger.debug(f"找到 {len(all_radios)} 个单选框")
                for i, radio in enumerate(all_radios[:20]):  # 只显示前20个
                    value = await radio.get_attribute("value")
                    name = await radio.get_attribute("name")
                    checked = await radio.get_attribute("checked")
                    self.logger.debug(f"  [{i}] value={value}, name={name}, checked={checked}")

                # 调试：输出所有包含"Method"的label
                self.logger.debug("=== 调试信息：包含'Method'的label ===")
                method_labels = await self.page.locator(self.METHOD_LABELS_SELECTOR).all()
                self.logger.debug(f"找到 {len(method_labels)} 个匹配的label")
                for i, label in enumerate(method_labels):
                    text = await label.text_content()
                    self.logger.debug(f"  [{i}] text={text}")

                # 调试：尝试定位 "Method of Signing" label
                self.logger.debug(f"=== 尝试定位: label:has-text('{self.METHOD_OF_SIGNING_LABEL}') ===")
                try:
                    method_label_element = await self.page.locator(f"label:has-text('{self.METHOD_OF_SIGNING_LABEL}')").first.wait_for(timeout=5000)
                    self.logger.debug("✓ 找到了标签")
                except Exception as e:
                    self.logger.debug(f"✗ 未找到标签: {str(e)}")

                # 通过 label 文本定位，找到包含 value=2 的 radio
                private_radio = self.page.locator(f"label:has-text('{self.METHOD_OF_SIGNING_LABEL}')").locator("..").locator(f"input[type='radio'][value='{self.PRIVATE_RFP_VALUE}']")
                await private_radio.click()
                self.logger.debug(f"Private RFP (value={self.PRIVATE_RFP_VALUE}) 已选中")
                allure.attach("已选择: Private RFP", "签约方式")
                self.logger.info("Private RFP 已选中")
            except Exception as e:
                error_msg = f"选择签约方式失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "选择错误")
                raise

    async def select_notification_method(self) -> None:
        """选择通知方式: Manual Notification (value=0)"""
        self.logger.info("开始选择通知方式: Manual Notification")

        with allure.step("选择通知方式: Manual Notification"):
            try:
                # 定位到对应 label，再找 value=0 的 radio
                manual_radio = self.page.locator(f"label:has-text('{self.NOTIFICATION_METHOD_LABEL}')").locator("..").locator(f"input[type='radio'][value='{self.MANUAL_NOTIFICATION_VALUE}']")
                await manual_radio.click()
                self.logger.debug(f"Manual Notification (value={self.MANUAL_NOTIFICATION_VALUE}) 已选中")
                allure.attach("已选择: Manual Notification", "通知方式")
                self.logger.info("Manual Notification 已选中")
            except Exception as e:
                error_msg = f"选择通知方式失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "选择错误")
                raise

    async def handle_quotation_reports(self) -> None:
        """设置报价报告为 NO NEED (value=0)"""
        self.logger.info("开始设置报价报告为 NO NEED")

        with allure.step("设置报价报告为 NO NEED"):
            try:
                # 设置 GROUP QUOTATION STATUS REPORT 为 NO NEED
                group_radio = self.page.locator(f"label:has-text('{self.GROUP_QUOTATION_LABEL}')").locator("..").locator(f"input[type='radio'][value='{self.GROUP_QUOTATION_VALUE}']")
                await group_radio.click()
                self.logger.debug(f"GROUP QUOTATION STATUS REPORT 已设置为 NO NEED")

                # 设置 Enterprise Quotation Status Report 为 NO NEED
                enterprise_radio = self.page.locator(f"label:has-text('{self.ENTERPRISE_QUOTATION_LABEL}')").locator("..").locator(f"input[type='radio'][value='{self.ENTERPRISE_QUOTATION_VALUE}']")
                await enterprise_radio.click()
                self.logger.debug(f"Enterprise Quotation Status Report 已设置为 NO NEED")

                allure.attach(f"GROUP QUOTATION STATUS: NO NEED\nEnterprise Quotation Status: NO NEED", "报价报告设置")
                self.logger.info("报价报告设置成功")
            except Exception as e:
                error_msg = f"设置报价报告失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "设置错误")
                raise

    # ========== 日期选择方法 ==========
    async def select_bidding_dates(self, start_date: str, end_date: str) -> None:
        """
        选择三个日期范围：
        1. Bidding Date Range
        2. Registration Period
        3. First Round Bidding Period

        Args:
            start_date: 开始日期 (格式: YYYY-MM-DD, 例: 2026-04-10)
            end_date: 结束日期 (格式: YYYY-MM-DD, 例: 2026-05-10)
        """
        self.logger.info(f"开始选择日期范围: {start_date} ~ {end_date}")

        with allure.step(f"选择日期范围: {start_date} ~ {end_date}"):
            try:
                # 获取所有日期选择器（placeholder='Please select' 的 input）
                date_pickers = await self.page.get_by_placeholder(self.DATE_PICKER_PLACEHOLDER).all()

                # 预期的日期选择器数量（3个范围，每个2个开始/结束）
                expected_count = 6
                if len(date_pickers) < expected_count:
                    raise Exception(f"找到的日期选择器不足：{len(date_pickers)} 个，需要至少 {expected_count} 个")

                # 三个日期范围配置
                date_ranges = [
                    ("Bidding Date Range", self.BIDDING_DATE_START_IDX, self.BIDDING_DATE_END_IDX),
                    ("Registration Period", self.REGISTRATION_START_IDX, self.REGISTRATION_END_IDX),
                    ("First Round Bidding Period", self.FIRST_ROUND_START_IDX, self.FIRST_ROUND_END_IDX)
                ]

                for range_name, start_idx, end_idx in date_ranges:
                    self.logger.debug(f"填充 {range_name}: {start_date} ~ {end_date}")

                    start_picker = date_pickers[start_idx]
                    end_picker = date_pickers[end_idx]

                    await start_picker.fill(start_date)
                    self.logger.debug(f"  开始日期已填充: {start_date}")

                    await end_picker.fill(end_date)
                    self.logger.debug(f"  结束日期已填充: {end_date}")

                allure.attach(
                    f"Bidding Date Range: {start_date} ~ {end_date}\n"
                    f"Registration Period: {start_date} ~ {end_date}\n"
                    f"First Round Bidding Period: {start_date} ~ {end_date}",
                    "日期范围"
                )
                self.logger.info(f"三个日期范围选择成功: {start_date} ~ {end_date}")
            except Exception as e:
                error_msg = f"选择日期范围失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "日期选择错误")
                raise


    # ========== 数量输入方法 ==========
    async def fill_expected_hotels_count(self) -> int:
        """填写预期合同酒店数量（随机生成 1-50）"""
        self.logger.info("开始填写预期合同酒店数量")

        with allure.step("填写预期合同酒店数量"):
            try:
                hotels_count = self._generate_random_hotels_count()
                self.logger.debug(f"生成随机酒店数量: {hotels_count}")

                # 使用 getByLabel() 定位
                count_input = self.page.get_by_label(self.EXPECTED_HOTELS_COUNT_LABEL)
                await count_input.fill(str(hotels_count))

                allure.attach(f"预期合同酒店数量: {hotels_count}", "酒店数量")
                self.logger.info(f"预期合同酒店数量填写成功: {hotels_count}")
                return hotels_count
            except Exception as e:
                error_msg = f"填写酒店数量失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "填充错误")
                raise

    # ========== 提交和验证方法 ==========
    async def click_save_button(self) -> None:
        """点击保存按钮"""
        self.logger.info("开始点击保存按钮")

        with allure.step("点击保存按钮"):
            try:
                # 使用 getByRole() 定位 Save 按钮 - 最稳定
                save_btn = self.page.get_by_role("button", name=self.SAVE_BUTTON_NAME)
                await save_btn.click()

                # 等待页面响应
                self.logger.debug("等待页面响应")
                await self.page.wait_for_load_state("networkidle", timeout=timeout_config.get_navigation_timeout())

                allure.attach("保存按钮已点击", "操作结果")
                self.logger.info("保存按钮已点击，等待响应")
            except Exception as e:
                error_msg = f"点击保存按钮失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "点击错误")
                raise

    async def verify_save_success(self) -> bool:
        """验证保存成功（检查成功提示信息）"""
        self.logger.info("开始验证保存成功")

        with allure.step("验证保存成功提示"):
            try:
                # 等待成功提示出现
                self.logger.debug(f"等待成功提示: {self.SUCCESS_MESSAGE_SELECTOR}")
                await self.wait_helper.wait_for_selector(
                    self.page,
                    self.SUCCESS_MESSAGE_SELECTOR,
                    timeout=timeout_config.get_element_timeout()
                )

                # 获取提示文本
                success_msg = await self.page.locator(self.SUCCESS_MESSAGE_SELECTOR).text_content()
                self.logger.info(f"成功提示已出现: {success_msg}")

                # 验证提示是否可见
                is_visible = await self.page.locator(self.SUCCESS_MESSAGE_SELECTOR).is_visible()

                allure.attach(f"成功提示: {success_msg}\n可见: {is_visible}", "验证结果")
                self.logger.info(f"保存成功验证完成: {is_visible}")
                return is_visible
            except Exception as e:
                error_msg = f"验证保存成功失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach(error_msg, "验证错误")
                return False
