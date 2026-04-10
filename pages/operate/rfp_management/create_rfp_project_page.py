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
    RFP_MANAGEMENT_MENU = "div.el-menu >> text=RFP Management"
    CREATE_NEW_RFP_PROJECT_MENU = "div.el-menu >> text=Create new RFP project"

    # ========== 表单字段元素 ==========
    ORGANIZATION_NAME_INPUT = "input[name='organizationName']"
    PROJECT_NAME_INPUT = "input[name='projectName']"
    CONTACT_PERSON_INPUT = "input[name='contactPerson']"
    AREA_CODE_INPUT = "input[name='areaCode']"
    PHONE_NUMBER_INPUT = "input[name='phoneNumber']"

    # ========== 单选框和下拉菜单 ==========
    PRIVATE_RFP_RADIO = "input[type='radio'][value='PRIVATE_RFP']"
    MANUAL_NOTIFICATION_OPTION = ".el-select >> text=Manual Notification"
    GROUP_QUOTATION_NO_NEED = "input[name='groupQuotation'][value='NO_NEED']"
    ENTERPRISE_QUOTATION_NO_NEED = "input[name='enterpriseQuotation'][value='NO_NEED']"

    # ========== 日期选择器 ==========
    BIDDING_DATE_START_PICKER = "input[name='biddingDateStart']"
    BIDDING_DATE_END_PICKER = "input[name='biddingDateEnd']"
    REGISTRATION_DATE_START_PICKER = "input[name='registrationDateStart']"
    REGISTRATION_DATE_END_PICKER = "input[name='registrationDateEnd']"
    BIDDING_ROUND_DATE_START_PICKER = "input[name='roundDateStart']"
    BIDDING_ROUND_DATE_END_PICKER = "input[name='roundDateEnd']"

    # ========== 其他字段 ==========
    EXPECTED_HOTELS_COUNT_INPUT = "input[name='expectedHotelsCount']"
    SAVE_BUTTON = "button:has-text('Save') >> visible=true"
    SUCCESS_MESSAGE_CONTAINER = ".el-message__content"

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
                await self.wait_helper.wait_for_selector(
                    self.page,
                    self.ORGANIZATION_NAME_INPUT,
                    timeout=timeout_config.get_navigation_timeout()
                )

                allure.attach_text("导航成功，表单已加载", "导航结果")
                self.logger.info("导航成功，创建新 RFP 项目表单已加载")

            except Exception as e:
                error_msg = f"导航至创建页面失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach_text(error_msg, "导航错误")
                raise

    # ========== 表单填充方法 ==========
    async def fill_organization_name(self, org_name: str = "hyg测试机构") -> None:
        """填写组织名称"""
        self.logger.info(f"开始填写组织名称: {org_name}")

        with allure.step(f"填写组织名称: {org_name}"):
            try:
                self.logger.debug(f"查找组织名称输入框: {self.ORGANIZATION_NAME_INPUT}")
                org_input = await self.find_element(self.ORGANIZATION_NAME_INPUT)
                await org_input.fill(org_name)
                allure.attach_text(f"组织名称: {org_name}", "填充数据")
                self.logger.info(f"组织名称填写成功: {org_name}")
            except Exception as e:
                error_msg = f"填写组织名称失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach_text(error_msg, "填充错误")
                raise

    async def fill_project_name(self) -> str:
        """填写项目名称（自动生成）"""
        self.logger.info("开始填写项目名称")

        with allure.step("填写项目名称"):
            try:
                timestamp = self._generate_timestamp()
                project_name = f"hyg-自动化项目-{timestamp}"

                self.logger.debug(f"查找项目名称输入框: {self.PROJECT_NAME_INPUT}")
                project_input = await self.find_element(self.PROJECT_NAME_INPUT)
                await project_input.fill(project_name)

                allure.attach_text(f"生成的项目名称: {project_name}", "项目名称")
                self.logger.info(f"项目名称填写成功: {project_name}")
                return project_name
            except Exception as e:
                error_msg = f"填写项目名称失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach_text(error_msg, "填充错误")
                raise

    async def fill_contact_person(self, person: str = "荷叶") -> None:
        """填写联系人"""
        self.logger.info(f"开始填写联系人: {person}")

        with allure.step(f"填写联系人: {person}"):
            try:
                self.logger.debug(f"查找联系人输入框: {self.CONTACT_PERSON_INPUT}")
                contact_input = await self.find_element(self.CONTACT_PERSON_INPUT)
                await contact_input.fill(person)
                allure.attach_text(f"联系人: {person}", "填充数据")
                self.logger.info(f"联系人填写成功: {person}")
            except Exception as e:
                error_msg = f"填写联系人失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach_text(error_msg, "填充错误")
                raise

    async def fill_contact_number(self, area_code: str, phone: str) -> None:
        """填写联系电话（区号 + 电话号码分两个字段）"""
        self.logger.info(f"开始填写联系电话: {area_code} {phone}")

        with allure.step(f"填写联系电话: {area_code} {phone}"):
            try:
                # 填写区号
                self.logger.debug(f"查找区号输入框: {self.AREA_CODE_INPUT}")
                area_input = await self.find_element(self.AREA_CODE_INPUT)
                await area_input.fill(area_code)
                self.logger.debug(f"区号填写成功: {area_code}")

                # 填写电话号码
                self.logger.debug(f"查找电话号码输入框: {self.PHONE_NUMBER_INPUT}")
                phone_input = await self.find_element(self.PHONE_NUMBER_INPUT)
                await phone_input.fill(phone)
                self.logger.debug(f"电话号码填写成功: {phone}")

                allure.attach_text(f"区号: {area_code}, 电话: {phone}", "联系电话")
                self.logger.info(f"联系电话填写成功: {area_code} {phone}")
            except Exception as e:
                error_msg = f"填写联系电话失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach_text(error_msg, "填充错误")
                raise

    # ========== 选择器方法 ==========
    async def select_signing_method(self) -> None:
        """选择签约方式: Private RFP"""
        self.logger.info("开始选择签约方式: Private RFP")

        with allure.step("选择签约方式: Private RFP"):
            try:
                self.logger.debug(f"查找 Private RFP 单选框: {self.PRIVATE_RFP_RADIO}")
                private_radio = await self.find_element(self.PRIVATE_RFP_RADIO)
                await private_radio.click()
                allure.attach_text("已选择: Private RFP", "签约方式")
                self.logger.info("Private RFP 已选中")
            except Exception as e:
                error_msg = f"选择签约方式失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach_text(error_msg, "选择错误")
                raise

    async def select_notification_method(self) -> None:
        """选择通知方式: Manual Notification"""
        self.logger.info("开始选择通知方式: Manual Notification")

        with allure.step("选择通知方式: Manual Notification"):
            try:
                self.logger.debug(f"查找 Manual Notification 选项: {self.MANUAL_NOTIFICATION_OPTION}")
                notification_option = await self.find_element(self.MANUAL_NOTIFICATION_OPTION)
                await notification_option.click()
                allure.attach_text("已选择: Manual Notification", "通知方式")
                self.logger.info("Manual Notification 已选中")
            except Exception as e:
                error_msg = f"选择通知方式失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach_text(error_msg, "选择错误")
                raise

    async def handle_quotation_reports(self) -> None:
        """设置报价报告为 NO NEED"""
        self.logger.info("开始设置报价报告为 NO NEED")

        with allure.step("设置报价报告为 NO NEED"):
            try:
                # 设置 GROUP QUOTATION STATUS REPORT 为 NO NEED
                self.logger.debug(f"查找 GROUP QUOTATION 'NO NEED' 选项: {self.GROUP_QUOTATION_NO_NEED}")
                group_quota = await self.find_element(self.GROUP_QUOTATION_NO_NEED)
                await group_quota.click()
                self.logger.debug("GROUP QUOTATION STATUS REPORT 已设置为 NO NEED")

                # 设置 Enterprise Quotation Status Report 为 NO NEED
                self.logger.debug(f"查找 ENTERPRISE QUOTATION 'NO NEED' 选项: {self.ENTERPRISE_QUOTATION_NO_NEED}")
                enterprise_quota = await self.find_element(self.ENTERPRISE_QUOTATION_NO_NEED)
                await enterprise_quota.click()
                self.logger.debug("Enterprise Quotation Status Report 已设置为 NO NEED")

                allure.attach_text("GROUP QUOTATION STATUS: NO NEED\nEnterprise Quotation Status: NO NEED", "报价报告设置")
                self.logger.info("报价报告设置成功: 两个都设置为 NO NEED")
            except Exception as e:
                error_msg = f"设置报价报告失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach_text(error_msg, "设置错误")
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
                # 选择 Bidding Date Range
                self.logger.debug("开始选择 Bidding Date Range")
                await self._select_date_range(
                    self.BIDDING_DATE_START_PICKER,
                    self.BIDDING_DATE_END_PICKER,
                    start_date,
                    end_date,
                    "Bidding Date Range"
                )

                # 选择 Registration Period
                self.logger.debug("开始选择 Registration Period")
                await self._select_date_range(
                    self.REGISTRATION_DATE_START_PICKER,
                    self.REGISTRATION_DATE_END_PICKER,
                    start_date,
                    end_date,
                    "Registration Period"
                )

                # 选择 First Round Bidding Period
                self.logger.debug("开始选择 First Round Bidding Period")
                await self._select_date_range(
                    self.BIDDING_ROUND_DATE_START_PICKER,
                    self.BIDDING_ROUND_DATE_END_PICKER,
                    start_date,
                    end_date,
                    "First Round Bidding Period"
                )

                allure.attach_text(
                    f"Bidding Date Range: {start_date} ~ {end_date}\n"
                    f"Registration Period: {start_date} ~ {end_date}\n"
                    f"First Round Bidding Period: {start_date} ~ {end_date}",
                    "日期范围"
                )
                self.logger.info(f"三个日期范围选择成功: {start_date} ~ {end_date}")
            except Exception as e:
                error_msg = f"选择日期范围失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach_text(error_msg, "日期选择错误")
                raise

    async def _select_date_range(
        self,
        start_selector: str,
        end_selector: str,
        start_date: str,
        end_date: str,
        range_name: str
    ) -> None:
        """
        辅助方法：选择日期范围

        Args:
            start_selector: 开始日期选择器
            end_selector: 结束日期选择器
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            range_name: 日期范围名称（用于日志）
        """
        self.logger.debug(f"_select_date_range: {range_name} - {start_date} ~ {end_date}")

        try:
            # 尝试直接填充开始日期
            self.logger.debug(f"填充 {range_name} 开始日期: {start_date}")
            start_input = await self.find_element(start_selector)
            await start_input.fill(start_date)
            self.logger.debug(f"{range_name} 开始日期填充成功")

            # 尝试直接填充结束日期
            self.logger.debug(f"填充 {range_name} 结束日期: {end_date}")
            end_input = await self.find_element(end_selector)
            await end_input.fill(end_date)
            self.logger.debug(f"{range_name} 结束日期填充成功")

        except Exception as e:
            self.logger.warning(f"直接填充日期失败，尝试日历交互: {str(e)}")
            raise Exception(f"选择 {range_name} 日期失败: {str(e)}")

    # ========== 数量输入方法 ==========
    async def fill_expected_hotels_count(self) -> int:
        """填写预期合同酒店数量（随机生成 1-50）"""
        self.logger.info("开始填写预期合同酒店数量")

        with allure.step("填写预期合同酒店数量"):
            try:
                hotels_count = self._generate_random_hotels_count()
                self.logger.debug(f"生成随机酒店数量: {hotels_count}")

                self.logger.debug(f"查找酒店数量输入框: {self.EXPECTED_HOTELS_COUNT_INPUT}")
                count_input = await self.find_element(self.EXPECTED_HOTELS_COUNT_INPUT)
                await count_input.fill(str(hotels_count))

                allure.attach_text(f"预期合同酒店数量: {hotels_count}", "酒店数量")
                self.logger.info(f"预期合同酒店数量填写成功: {hotels_count}")
                return hotels_count
            except Exception as e:
                error_msg = f"填写酒店数量失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach_text(error_msg, "填充错误")
                raise

    # ========== 提交和验证方法 ==========
    async def click_save_button(self) -> None:
        """点击保存按钮"""
        self.logger.info("开始点击保存按钮")

        with allure.step("点击保存按钮"):
            try:
                self.logger.debug(f"查找保存按钮: {self.SAVE_BUTTON}")
                save_btn = await self.find_element(self.SAVE_BUTTON)
                await save_btn.click()

                # 等待页面响应
                self.logger.debug("等待页面响应")
                await self.page.wait_for_load_state("networkidle", timeout=timeout_config.get_navigation_timeout())

                allure.attach_text("保存按钮已点击", "操作结果")
                self.logger.info("保存按钮已点击，等待响应")
            except Exception as e:
                error_msg = f"点击保存按钮失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach_text(error_msg, "点击错误")
                raise

    async def verify_save_success(self) -> bool:
        """验证保存成功（检查成功提示信息）"""
        self.logger.info("开始验证保存成功")

        with allure.step("验证保存成功提示"):
            try:
                # 等待成功提示出现
                self.logger.debug(f"等待成功提示: {self.SUCCESS_MESSAGE_CONTAINER}")
                await self.wait_helper.wait_for_selector(
                    self.page,
                    self.SUCCESS_MESSAGE_CONTAINER,
                    timeout=timeout_config.get_element_timeout()
                )

                # 获取提示文本
                success_msg = await self.page.locator(self.SUCCESS_MESSAGE_CONTAINER).text_content()
                self.logger.info(f"成功提示已出现: {success_msg}")

                # 验证提示是否可见
                is_visible = await self.page.locator(self.SUCCESS_MESSAGE_CONTAINER).is_visible()

                allure.attach_text(f"成功提示: {success_msg}\n可见: {is_visible}", "验证结果")
                self.logger.info(f"保存成功验证完成: {is_visible}")
                return is_visible
            except Exception as e:
                error_msg = f"验证保存成功失败: {str(e)}"
                self.logger.error(error_msg)
                allure.attach_text(error_msg, "验证错误")
                return False
