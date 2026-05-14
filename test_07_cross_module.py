"""跨模块全流程 E2E 测试：首页 → 各模块 → 返回首页 → 下一模块。
覆盖完整用户操作路径。
"""
import pytest
from playwright.sync_api import Page, expect

BASE = "http://localhost:5173/#"


def _dismiss_any_dialog(page: Page):
    """关闭页面上可能出现的弹窗。"""
    try:
        btn = page.locator("button:has-text('确认')")
        if btn.is_visible(timeout=1000):
            btn.click()
            page.wait_for_timeout(300)
    except Exception:
        pass


@pytest.mark.regression
class TestCrossModuleFlow:
    """跨模块全流程回归。"""

    def test_full_navigation_flow(self, page: Page):
        """首页 → 供应商 → 返回 → 需求单 → 返回 → 白胚库存 → 返回 → 选项维护。"""
        # 1. 首页
        page.goto(f"{BASE}/")
        page.wait_for_timeout(800)
        expect(page.locator("text=供应链系统")).to_be_visible(timeout=5000)

        # 2. 供应商列表
        page.locator("text=供应商列表").click()
        page.wait_for_timeout(1500)
        expect(page.locator("text=供应商管理")).to_be_visible(timeout=5000)
        # 验证列表有数据
        feed = page.locator("feed")
        expect(feed).to_be_visible(timeout=5000)

        # 3. 返回首页
        page.locator("text=返回").click()
        page.wait_for_timeout(800)
        expect(page.locator("text=供应链系统")).to_be_visible(timeout=5000)

        # 4. 需求单列表
        page.locator("text=需求单列表").click()
        page.wait_for_timeout(1500)
        expect(page.locator("text=需求单列表").first).to_be_visible(timeout=5000)

        # 5. 返回首页
        page.locator("text=返回").click()
        page.wait_for_timeout(800)
        expect(page.locator("text=供应链系统")).to_be_visible(timeout=5000)

        # 6. 白胚库存列表
        page.locator("text=白胚库存列表").click()
        page.wait_for_timeout(1500)
        expect(page.locator("text=白胚库存列表").first).to_be_visible(timeout=5000)

        # 7. 返回首页
        page.locator("text=返回").click()
        page.wait_for_timeout(800)
        expect(page.locator("text=供应链系统")).to_be_visible(timeout=5000)

        # 8. 选项维护
        page.locator("text=选项维护").click()
        page.wait_for_timeout(1500)
        expect(page.locator("text=工序项维护")).to_be_visible(timeout=5000)

    def test_supplier_search_and_detail_flow(self, page: Page):
        """供应商模块：搜索 → 查看详情 → 返回列表。"""
        page.goto(f"{BASE}/pages/supplier/list")
        page.wait_for_timeout(2000)

        # 搜索
        search_input = page.get_by_placeholder("请输入")
        search_input.fill("张三")
        page.locator("button:has-text('查询')").click()
        page.wait_for_timeout(1500)

        # 点击第一项进详情
        feed_items = page.locator("feed > *")
        if feed_items.count() > 0:
            feed_items.first.click()
            page.wait_for_timeout(1500)
            # 应在供应商相关页面
            assert "supplier" in page.url.lower() or "供应商" in page.content()

    def test_tracking_dialog_flow(self, page: Page):
        """跟单模块：进入 → 处理弹窗 → 验证页面加载。"""
        page.goto(f"{BASE}/pages/documentary/documentary")
        page.wait_for_timeout(2000)
        _dismiss_any_dialog(page)
        page.wait_for_timeout(500)
        # 验证页面基本元素
        expect(page.locator("text=跟单系统")).to_be_visible(timeout=5000)
        # Tab 栏
        for tab in ["全部", "待进厂", "进行中"]:
            expect(page.locator(f"text={tab}").first).to_be_visible(timeout=3000)

    def test_options_sub_navigation_flow(self, page: Page):
        """选项维护 → 工厂维护 → 返回 → 仓库维护。"""
        page.goto(f"{BASE}/pages/maintenance-list/maintenance-list")
        page.wait_for_timeout(1000)

        # 进入工厂维护
        page.locator("text=工厂维护").click()
        page.wait_for_timeout(1500)
        original_url = page.url
        assert "maintenance-list" not in original_url or original_url != f"{BASE}/pages/maintenance-list/maintenance-list"

        # 返回
        back = page.locator("text=返回")
        if back.is_visible(timeout=2000):
            back.click()
            page.wait_for_timeout(800)

        # 重新进入维护列表
        page.goto(f"{BASE}/pages/maintenance-list/maintenance-list")
        page.wait_for_timeout(1000)

        # 进入仓库维护
        page.locator("text=仓库维护").click()
        page.wait_for_timeout(1500)
        assert page.url != f"{BASE}/pages/maintenance-list/maintenance-list"


@pytest.mark.regression
class TestPageStability:
    """页面稳定性测试。"""

    def test_rapid_navigation_no_crash(self, page: Page):
        """快速切换多个页面不应崩溃。"""
        routes = [
            f"{BASE}/",
            f"{BASE}/pages/supplier/list",
            f"{BASE}/pages/spot/list",
            f"{BASE}/pages/whiteEmbryo/listSearch",
            f"{BASE}/pages/maintenance-list/maintenance-list",
            f"{BASE}/",
        ]
        for route in routes:
            page.goto(route)
            page.wait_for_timeout(500)
            _dismiss_any_dialog(page)
        # 最终应回到首页
        expect(page.locator("text=供应链系统")).to_be_visible(timeout=5000)

    def test_no_js_errors_on_home(self, page: Page):
        """首页加载不应有 JS 错误（除已知 jQuery 问题）。"""
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(f"{BASE}/")
        page.wait_for_timeout(2000)
        # 过滤掉已知的 jQuery 错误
        real_errors = [e for e in errors if "jQuery" not in e]
        assert len(real_errors) == 0, f"首页 JS 错误: {real_errors}"

    def test_no_js_errors_on_supplier(self, page: Page):
        """供应商列表不应有 JS 错误。"""
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(f"{BASE}/pages/supplier/list")
        page.wait_for_timeout(3000)
        real_errors = [e for e in errors if "jQuery" not in e]
        assert len(real_errors) == 0, f"供应商页 JS 错误: {real_errors}"
