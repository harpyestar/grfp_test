"""
探索RFP表单元素定位器的脚本
用于验证页面中实际存在的元素和正确的定位方法
"""

import asyncio
import sys
from playwright.async_api import async_playwright
from utils.config import config
from utils.logger import get_logger

logger = get_logger("explore_rfp_form")


async def explore_form():
    """手动导航并探索表单元素"""

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=100)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})

        try:
            # Step 1: 登录
            logger.info("=" * 80)
            logger.info("Step 1: 登录到系统")
            logger.info("=" * 80)

            account = config.get_account("operate")
            login_url = f"{config.base_url}/login"

            logger.info(f"正在访问: {login_url}")
            await page.goto(login_url, timeout=60000)
            logger.info("页面已加载，等待form元素...")

            # 等待表单元素出现
            await page.wait_for_selector('input[type="text"]', timeout=60000)
            logger.info("表单元素已加载")

            # 填写登录表单
            await page.fill('input[type="text"]', account["email"])
            await page.fill('input[type="password"]', account["password"])
            await page.click('button:has-text("Login")')

            logger.info(f"正在登录: {account['email']}")
            await page.wait_for_url("**/home", timeout=15000)
            logger.info("✓ 登录成功")

            # 等待页面加载
            await page.wait_for_load_state("networkidle")
            await page.screenshot(path="/tmp/01_logged_in.png", full_page=True)
            logger.info("✓ 截图: /tmp/01_logged_in.png")

            # Step 2: 导航到RFP Management菜单
            logger.info("\n" + "=" * 80)
            logger.info("Step 2: 点击 RFP Management 菜单")
            logger.info("=" * 80)

            rfp_menu = page.get_by_text("RFP Management").first
            await rfp_menu.click()
            logger.info("✓ RFP Management 菜单已点击")

            await page.wait_for_timeout(500)

            # Step 3: 点击 Create new RFP project
            logger.info("\n" + "=" * 80)
            logger.info("Step 3: 点击 Create new RFP project")
            logger.info("=" * 80)

            create_menu = page.get_by_text("Create new RFP project").first
            await create_menu.click()
            logger.info("✓ Create new RFP project 已点击")

            # 等待表单加载
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(1000)

            await page.screenshot(path="/tmp/02_rfp_form.png", full_page=True)
            logger.info("✓ 截图: /tmp/02_rfp_form.png")

            # Step 4: 探索表单元素
            logger.info("\n" + "=" * 80)
            logger.info("Step 4: 探索表单元素")
            logger.info("=" * 80)

            # 查找所有input元素
            inputs = await page.locator("input").all()
            logger.info(f"\n找到 {len(inputs)} 个 input 元素:")
            for i, inp in enumerate(inputs[:30]):  # 只显示前30个
                input_type = await inp.get_attribute("type")
                name = await inp.get_attribute("name")
                placeholder = await inp.get_attribute("placeholder")
                aria_label = await inp.get_attribute("aria-label")
                logger.info(f"  [{i}] type={input_type}, name={name}, placeholder={placeholder}, aria-label={aria_label}")

            # 查找所有label元素
            labels = await page.locator("label").all()
            logger.info(f"\n找到 {len(labels)} 个 label 元素（前20个）:")
            for i, label in enumerate(labels[:20]):
                text = await label.text_content()
                for_attr = await label.get_attribute("for")
                if text and text.strip():
                    logger.info(f"  [{i}] text=\"{text.strip()[:60]}\", for=\"{for_attr}\"")

            # 查找所有button元素
            buttons = await page.locator("button").all()
            logger.info(f"\n找到 {len(buttons)} 个 button 元素:")
            for i, btn in enumerate(buttons[:15]):
                text = await btn.text_content()
                if text and text.strip():
                    logger.info(f"  [{i}] text=\"{text.strip()}\"")

            # 查找form-item元素（Element UI特定）
            form_items = await page.locator(".el-form-item").all()
            logger.info(f"\n找到 {len(form_items)} 个 form-item 元素:")
            for i, item in enumerate(form_items[:20]):
                label_elem = item.locator("label").first
                label_text = await label_elem.text_content() if label_elem else None
                if label_text:
                    logger.info(f"  [{i}] label=\"{label_text.strip()}\"")

            # Step 5: 尝试交互
            logger.info("\n" + "=" * 80)
            logger.info("Step 5: 测试表单交互")
            logger.info("=" * 80)

            # 尝试使用getByLabel定位
            logger.info("\n尝试 getByLabel('Organization Name'):")
            try:
                org_input = page.get_by_label("Organization Name")
                is_visible = await org_input.is_visible()
                logger.info(f"  ✓ 元素可见: {is_visible}")

                # 填写试试
                await org_input.fill("hyg测试机构")
                await page.wait_for_timeout(500)
                logger.info("  ✓ 已填入: hyg测试机构")

                # 查找自动完成选项
                autocomplete_items = await page.locator(".el-autocomplete-suggestion__list li").all()
                if autocomplete_items:
                    logger.info(f"  ✓ 找到 {len(autocomplete_items)} 个自动完成选项")
                    await autocomplete_items[0].click()
                    logger.info("  ✓ 已选择第一个选项")

            except Exception as e:
                logger.error(f"  ✗ 错误: {str(e)}")

            logger.info("\n尝试 getByLabel('Project name'):")
            try:
                project_input = page.get_by_label("Project name")
                is_visible = await project_input.is_visible()
                logger.info(f"  ✓ 元素可见: {is_visible}")
                await project_input.fill("hyg-自动化项目-test")
                logger.info("  ✓ 已填入: hyg-自动化项目-test")
            except Exception as e:
                logger.error(f"  ✗ 错误: {str(e)}")

            logger.info("\n尝试 getByLabel('Contact Person'):")
            try:
                contact_input = page.get_by_label("Contact Person")
                is_visible = await contact_input.is_visible()
                logger.info(f"  ✓ 元素可见: {is_visible}")
                await contact_input.fill("荷叶")
                logger.info("  ✓ 已填入: 荷叶")
            except Exception as e:
                logger.error(f"  ✗ 错误: {str(e)}")

            logger.info("\n尝试 getByPlaceholder('Area Code'):")
            try:
                area_input = page.get_by_placeholder("Area Code")
                is_visible = await area_input.is_visible()
                logger.info(f"  ✓ 元素可见: {is_visible}")
                await area_input.fill("010")
                logger.info("  ✓ 已填入: 010")
            except Exception as e:
                logger.error(f"  ✗ 错误: {str(e)}")

            logger.info("\n尝试单选框 - Method of Signing:")
            try:
                # 方法1: 通过label文本定位
                radio_options = await page.locator("label:has-text('Private RFP')").all()
                if radio_options:
                    logger.info(f"  找到 {len(radio_options)} 个匹配 'Private RFP' 的label")
                    # 点击对应的radio
                    parent = radio_options[0]
                    radio = parent.locator("..")
                    await radio.click()
                    logger.info("  ✓ 已点击 Private RFP")
            except Exception as e:
                logger.error(f"  ✗ 错误: {str(e)}")

            # 截图验证填充结果
            await page.screenshot(path="/tmp/03_form_filled.png", full_page=True)
            logger.info("\n✓ 截图: /tmp/03_form_filled.png")

            logger.info("\n" + "=" * 80)
            logger.info("探索完成！已保存3张截图:")
            logger.info("  1. /tmp/01_logged_in.png - 登录后的首页")
            logger.info("  2. /tmp/02_rfp_form.png - RFP表单页面")
            logger.info("  3. /tmp/03_form_filled.png - 填充后的表单")
            logger.info("=" * 80)

            # 保留浏览器打开供手动检查
            logger.info("\n按回车键关闭浏览器...")
            input()

        except Exception as e:
            logger.error(f"错误: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(explore_form())
