"""首页 + 导航冒烟测试：验证所有模块入口可达。"""
import pytest
from playwright.sync_api import Page, expect

BASE = "http://localhost:5173/#"

# 首页所有模块入口及对应路由
HOME_MODULES = [
    ("白胚库存列表", "/pages/whiteEmbryo/listSearch"),
    ("白胚入库", None),
    ("白胚扫码放货架", None),
    ("白胚列表", None),
    ("白胚库存等级列表", None),
    ("跟单列表", "/pages/documentary/documentary"),
    ("需求单列表", "/pages/spot/list"),
    ("定做单列表", None),
    ("待配货列表", None),
    ("色胚质检列表", None),
    ("手动质检列表", None),
    ("订单状态查询", None),
    ("面料编号打印", None),
    ("白胚质检列表", None),
    ("供应商列表", "/pages/supplier/list"),
    ("员工排班管理", None),
    ("询价列表", None),
    ("库存中心", None),
    ("打样收货列表", None),
    ("库存缺货", None),
    ("选项维护", "/pages/maintenance-list/maintenance-list"),
]


@pytest.mark.smoke
@pytest.mark.home
class TestHomePage:
    """首页基本功能验证。"""

    def test_home_page_title(self, page: Page):
        """首页标题应为「供应链系统」。"""
        page.goto(f"{BASE}/")
        expect(page.locator("text=供应链系统")).to_be_visible(timeout=5000)

    def test_home_all_module_entries_visible(self, page: Page):
        """首页所有模块入口应可见。"""
        page.goto(f"{BASE}/")
        page.wait_for_timeout(500)
        for name, _ in HOME_MODULES:
            entry = page.locator(f"text={name}")
            expect(entry).to_be_visible(timeout=3000)

    @pytest.mark.parametrize(
        "module_name,expected_route",
        [(n, r) for n, r in HOME_MODULES if r is not None],
        ids=[n for n, r in HOME_MODULES if r is not None],
    )
    def test_module_navigation(self, page: Page, module_name: str, expected_route: str):
        """点击模块入口应导航到正确路由。"""
        page.goto(f"{BASE}/")
        page.wait_for_timeout(300)
        page.locator(f"text={module_name}").click()
        page.wait_for_timeout(800)
        # 检查 URL 包含预期路由
        assert expected_route in page.url, f"点击 {module_name} 后 URL={page.url}，预期包含 {expected_route}"
        # 处理可能弹出的对话框
        dialog_btn = page.locator("button:has-text('确认')")
        if dialog_btn.is_visible():
            dialog_btn.click()
