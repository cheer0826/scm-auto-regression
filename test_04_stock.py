"""白胚库存模块 E2E 测试。
流程：进入列表 → 品类筛选 → 验证表头 → 返回。
"""
import pytest
from playwright.sync_api import Page, expect

BASE = "http://localhost:5173/#"


@pytest.mark.regression
@pytest.mark.stock
class TestWhiteEmbryoStock:
    """白胚库存列表。"""

    def test_stock_list_loads(self, page: Page):
        """白胚库存列表应正确加载。"""
        page.goto(f"{BASE}/pages/whiteEmbryo/listSearch")
        page.wait_for_timeout(1500)
        expect(page.locator("text=白胚库存列表")).to_be_visible(timeout=5000)

    def test_stock_category_filter_visible(self, page: Page):
        """品类筛选器应可见。"""
        page.goto(f"{BASE}/pages/whiteEmbryo/listSearch")
        page.wait_for_timeout(1000)
        expect(page.locator("text=品类:")).to_be_visible(timeout=3000)

    def test_stock_column_headers(self, page: Page):
        """表头应包含面料名称、匹数、米数。"""
        page.goto(f"{BASE}/pages/whiteEmbryo/listSearch")
        page.wait_for_timeout(1000)
        for header in ["面料名称", "面料匹数", "面料米数"]:
            expect(page.locator(f"text={header}").first).to_be_visible(timeout=3000)

    def test_stock_back_to_home(self, page: Page):
        """返回首页。"""
        page.goto(f"{BASE}/pages/whiteEmbryo/listSearch")
        page.wait_for_timeout(800)
        page.locator("text=返回").click()
        page.wait_for_timeout(800)
        assert page.url.endswith("/#/") or page.url.endswith("/#")
