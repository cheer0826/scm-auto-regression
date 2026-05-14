"""需求单模块全流程 E2E 测试。
流程：进入列表 → 验证筛选区 → 查看列表。
"""
import pytest
from playwright.sync_api import Page, expect

BASE = "http://localhost:5173/#"


@pytest.mark.regression
@pytest.mark.demand
class TestDemandOrderFlow:
    """需求单全流程。"""

    def test_demand_list_loads(self, page: Page):
        """需求单列表应正确加载。"""
        page.goto(f"{BASE}/pages/spot/list")
        page.wait_for_timeout(1500)
        expect(page.locator("text=需求单列表")).to_be_visible(timeout=5000)
        # 应有新增按钮
        expect(page.locator("text=新增需求单")).to_be_visible()

    def test_demand_filter_fields_visible(self, page: Page):
        """需求单筛选区各字段应可见。"""
        page.goto(f"{BASE}/pages/spot/list")
        page.wait_for_timeout(1000)
        for label in ["开始时间:", "截止时间:", "颜色筛选:", "订单状态:", "做单人员:", "是否作废:"]:
            expect(page.locator(f"text={label}")).to_be_visible(timeout=3000)

    def test_demand_column_headers(self, page: Page):
        """需求单列表表头应正确显示。"""
        page.goto(f"{BASE}/pages/spot/list")
        page.wait_for_timeout(1000)
        for header in ["日期/颜色", "面料名称/工艺", "匹数", "操作"]:
            expect(page.locator(f"text={header}").first).to_be_visible(timeout=3000)

    def test_demand_back_to_home(self, page: Page):
        """从需求单列表返回首页。"""
        page.goto(f"{BASE}/pages/spot/list")
        page.wait_for_timeout(800)
        page.locator("text=返回").click()
        page.wait_for_timeout(800)
        assert page.url.endswith("/#/") or page.url.endswith("/#")
