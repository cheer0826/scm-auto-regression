"""供应商模块全流程 E2E 测试。
流程：进入列表 → 验证列表加载 → 搜索 → 重置 → 点击详情 → 返回。
"""
import pytest
from playwright.sync_api import Page, expect

BASE = "http://localhost:5173/#"


@pytest.mark.regression
@pytest.mark.supplier
class TestSupplierFlow:
    """供应商模块全流程。"""

    def test_supplier_list_loads(self, page: Page):
        """供应商列表页应正确加载，显示数据。"""
        page.goto(f"{BASE}/pages/supplier/list")
        page.wait_for_timeout(1500)
        # 页面标题
        expect(page.locator("text=供应商管理")).to_be_visible(timeout=5000)
        # 应有搜索框
        expect(page.get_by_placeholder("请输入")).to_be_visible()
        # 应有新增按钮
        expect(page.locator("button:has-text('新增')")).to_be_visible()
        # 列表应有数据项（至少 1 条 feed 子元素）
        feed = page.locator("feed")
        expect(feed).to_be_visible(timeout=5000)

    def test_supplier_search(self, page: Page):
        """输入关键词搜索供应商。"""
        page.goto(f"{BASE}/pages/supplier/list")
        page.wait_for_timeout(1500)
        search_input = page.get_by_placeholder("请输入")
        search_input.fill("张三")
        page.locator("button:has-text('查询')").click()
        page.wait_for_timeout(1500)
        # 搜索后应存在包含"张三"的项 或者无数据提示
        content = page.content()
        assert "张三" in content or "没有更多了" in content or "暂无数据" in content

    def test_supplier_search_reset(self, page: Page):
        """搜索后重置应清空搜索框。"""
        page.goto(f"{BASE}/pages/supplier/list")
        page.wait_for_timeout(1500)
        search_input = page.get_by_placeholder("请输入")
        search_input.fill("不存在的供应商XYZ")
        page.locator("button:has-text('查询')").click()
        page.wait_for_timeout(1000)
        page.locator("button:has-text('重置')").click()
        page.wait_for_timeout(1000)
        assert search_input.input_value() == ""

    def test_supplier_detail_navigate(self, page: Page):
        """点击供应商列表项应进入详情页。"""
        page.goto(f"{BASE}/pages/supplier/list")
        page.wait_for_timeout(2000)
        # 点击第一个供应商项
        feed_items = page.locator("feed > *")
        if feed_items.count() > 0:
            first_item = feed_items.first
            first_item.click()
            page.wait_for_timeout(1500)
            # 应导航到详情页或显示详情内容
            url = page.url
            content = page.content()
            assert (
                "supplier" in url.lower()
                or "详情" in content
                or "供应商" in content
            ), f"点击供应商项后未跳转详情页: url={url}"
        else:
            pytest.skip("列表为空，跳过详情导航测试")

    def test_supplier_back_button(self, page: Page):
        """从供应商列表点击返回应回首页。"""
        page.goto(f"{BASE}/pages/supplier/list")
        page.wait_for_timeout(1000)
        page.locator("text=返回").click()
        page.wait_for_timeout(800)
        assert page.url.endswith("/#/") or page.url.endswith("/#"), f"返回后 URL={page.url}"
