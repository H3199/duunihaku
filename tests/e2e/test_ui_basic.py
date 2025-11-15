import pytest

@pytest.mark.playwright
def test_page_load(page, base_url):
    page.goto(base_url)

    # Check title exists
    page.wait_for_selector("h1", timeout=5000)
    assert "Daily Job Listings Dashboard" in page.inner_text("h1")

    # Wait until jobs render
    page.wait_for_selector("div[data-testid='stMarkdownContainer']", timeout=8000)

    # Ensure at least one job element exists
    assert page.locator("text=Company:").count() > 0

@pytest.mark.playwright
def test_tabs(page, base_url):
    page.goto(base_url)

    # Wait for headers to load
    page.wait_for_selector("h1", timeout=10000)

    assert page.locator("text=Applied Jobs").first.is_visible()
    assert page.locator("text=Remote Jobs").first.is_visible()

    page.click("text=🇪🇺 Remote Jobs")

    # Wait for content to update
    page.wait_for_timeout(800)

    emea_jobs = page.locator("text=Company:").count()
    assert emea_jobs > 0, "Expected jobs in EMEA tab, found 0."

    # ---- Switch back to FI ----
#    page.click("text=🇫🇮 Jobs")

#    page.wait_for_timeout(800)

#    fi_jobs_after = page.locator("text=Company:").count()
#    assert fi_jobs_after > 0
#    assert fi_jobs_after == fi_jobs_before
