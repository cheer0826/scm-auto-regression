"""跟单系统模块 E2E 测试。
流程：进入页面 → 处理弹窗 → 验证筛选区 → 验证 tab 栏。
"""
import pytest
from playwright.sync_api import Page, expect

BASE = "http://localhost:5173/#"


@pytest.mark.regression
@pytest.mark.tracking
class TestTrackingFlow:
    """跟单系统全流程。"""

    def _dismiss_dialog(self, page: Page):
        """关闭可能出现的'必须先选择染厂'弹窗。"""
        try:
            btn = page.locator("button:has-text('确认')")
            if btn.is_visible(timeout=2000):
                btn.click()
                page.wait_for_timeout(300)
        except Exception:
            pass

    def test_tracking_page_loads(self, page: Page):
        """跟单列表页应正确加载。"""
        page.goto(f"{BASE}/pages/documentary/documentary")
        page.wait_for_timeout(1500)
        self._dismiss_dialog(page)
        expect(page.locator("text=跟单系统")).to_be_visible(timeout=5000)

    def test_tracking_filter_fields(self, page: Page):
        """跟单筛选区字段应可见。"""
        page.goto(f"{BASE}/pages/documentary/documentary")
        page.wait_for_timeout(1500)
        self._dismiss_dialog(page)
        for label in ["选择工厂:", "更新状态:", "开始时间:", "截止时间:", "面料名称:", "颜色色号:"]:
            expect(page.locator(f"text={label}")).to_be_visible(timeout=3000)

    def test_tracking_tab_bar(self, page: Page):
        """底部 tab 栏应包含全部/待进厂/进行中/待出厂/已出厂。"""
        page.goto(f"{BASE}/pages/documentary/documentary")
        page.wait_for_timeout(1500)
        self._dismiss_dialog(page)
        for tab in ["全部", "待进厂", "进行中", "待出厂", "已出厂"]:
            expect(page.locator(f"text={tab}").first).to_be_visible(timeout=3000)

    def test_tracking_table_header(self, page: Page):
        """列表表头应包含面料/颜色、状态。"""
        page.goto(f"{BASE}/pages/documentary/documentary")
        page.wait_for_timeout(1500)
        self._dismiss_dialog(page)
        expect(page.locator("text=面料/颜色").first).to_be_visible(timeout=3000)
        expect(page.locator("text=状态").first).to_be_visible(timeout=3000)
