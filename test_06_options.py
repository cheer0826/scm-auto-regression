"""选项维护模块 E2E 测试。
流程：进入维护列表 → 验证所有子选项可见 → 点击子选项进入 → 返回。
"""
import pytest
from playwright.sync_api import Page, expect

BASE = "http://localhost:5173/#"

# 选项维护子模块
MAINTENANCE_OPTIONS = [
    "工序项维护", "工艺要求维护", "白胚等级维护", "供应商维护",
    "工厂维护", "其他要求项维护", "理化报告选项维护", "工艺流程维护",
    "工艺维护", "仓库维护", "库位号维护", "色胚质检瑕疵维护",
    "单匹面料瑕疵维护", "色胚质检项维护", "回修原因维护", "定做颜色维护",
    "工艺单工艺维护", "品名维护", "白胚疵点维护", "色差等级维护",
    "机器型号维护", "供应商性质维护", "色差基准色维护", "质量要求维护",
    "结账周期维护", "面料状态维护", "毛点选项维护", "色胚审核问题维护",
]


@pytest.mark.regression
@pytest.mark.options
class TestOptionsMaintenanceFlow:
    """选项维护全流程。"""

    def test_options_page_loads(self, page: Page):
        """选项维护首页应正确加载。"""
        page.goto(f"{BASE}/pages/maintenance-list/maintenance-list")
        page.wait_for_timeout(1500)
        # 至少第一个选项可见
        expect(page.locator("text=工序项维护")).to_be_visible(timeout=5000)

    @pytest.mark.parametrize("option_name", MAINTENANCE_OPTIONS[:10],
                             ids=MAINTENANCE_OPTIONS[:10])
    def test_option_entry_visible(self, page: Page, option_name: str):
        """各维护选项入口应可见。"""
        page.goto(f"{BASE}/pages/maintenance-list/maintenance-list")
        page.wait_for_timeout(1000)
        expect(page.locator(f"text={option_name}")).to_be_visible(timeout=3000)

    def test_option_sub_navigate(self, page: Page):
        """点击维护子项应跳转到子页面。"""
        page.goto(f"{BASE}/pages/maintenance-list/maintenance-list")
        page.wait_for_timeout(1000)
        page.locator("text=工厂维护").click()
        page.wait_for_timeout(1500)
        current_url = page.url
        # 应跳转到子页面
        assert current_url != f"{BASE}/pages/maintenance-list/maintenance-list", \
            "点击工厂维护后应跳转"

    def test_option_count(self, page: Page):
        """选项维护页应包含至少 20 个选项。"""
        page.goto(f"{BASE}/pages/maintenance-list/maintenance-list")
        page.wait_for_timeout(1000)
        # 统计页面中"维护"文字出现次数
        items = page.locator("p:has-text('维护')")
        assert items.count() >= 20, f"维护选项只有 {items.count()} 个，预期 >=20"
