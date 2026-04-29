import os
from pathlib import Path

from playwright.sync_api import Browser, BrowserContext

PROJECT_ROOT = Path(__file__).resolve().parents[2]
VIDEO_DIR = PROJECT_ROOT / "videos"

BROWSER_CONTEXT_ARGS = {
    "base_url": os.getenv("BASE_APP_URL"),
    "viewport": {"width": 1320, "height": 980},
    "locale": "uk-UA",
    "timezone_id": "Europe/Kyiv",
    # "record_video_dir": str(VIDEO_DIR),
    "permissions": ["geolocation"],
}


def build_browser_context(
    browser: Browser,
    base_url: str,
    storage_state_path: Path | None = None,
) -> BrowserContext:
    kwargs = {
        **BROWSER_CONTEXT_ARGS,
        "base_url": base_url,
    }
    if storage_state_path and storage_state_path.exists():
        kwargs["storage_state"] = str(storage_state_path)
    return browser.new_context(**kwargs)
