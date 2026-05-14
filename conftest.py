"""前端 E2E 自动化回归测试 — Playwright conftest."""
import pytest
from playwright.sync_api import Page

BASE_URL = "http://localhost:5173/#"

# 登录凭证（OAuth）
OAUTH_URL = "http://120.26.196.222:7000/v1/auth/login"
USERNAME = "郭银慧"
PASSWORD = "252566"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 414, "height": 896},  # 移动端视口（UniApp）
        "locale": "zh-CN",
    }


@pytest.fixture(scope="session")
def _auth_token():
    """通过 OAuth 获取 token，整个会话复用。"""
    import requests
    resp = requests.post(
        OAUTH_URL,
        json={"username": USERNAME, "password": PASSWORD},
        timeout=15,
    )
    data = resp.json()
    token = data.get("data", {}).get("token") or data.get("token")
    if not token:
        pytest.skip(f"登录失败: {data}")
    return token


@pytest.fixture(scope="session")
def browser_context_args(_auth_token, browser_context_args):
    """在浏览器上下文中注入 token 到 localStorage。"""
    return {
        **browser_context_args,
        "viewport": {"width": 414, "height": 896},
        "locale": "zh-CN",
        "storage_state": None,
    }


@pytest.fixture(autouse=True)
def _inject_token(page: Page, _auth_token: str):
    """每个测试前注入 token 到 localStorage。"""
    page.goto(f"{BASE_URL}/")
    page.evaluate(f"""() => {{
        localStorage.setItem('token', '{_auth_token}');
        localStorage.setItem('Authorization', 'Bearer {_auth_token}');
    }}""")
    page.goto(f"{BASE_URL}/")
    page.wait_for_timeout(500)


def wait_for_list_load(page: Page, timeout: int = 5000):
    """等待列表加载完成（loading消失或数据出现）。"""
    try:
        page.wait_for_selector("text=加载中", state="hidden", timeout=timeout)
    except Exception:
        pass
    page.wait_for_timeout(300)
