"""
Automated Screenshot Engine for E2EE AI Chatbot Threat Modeler.
Uses Playwright with Microsoft Edge to navigate the running Streamlit app and capture:
- image1.png: STRIDE Threat Model
- image2.png: Risk Analysis / Risk Simulator
- image3.png: Mitigation Controls / Traceability Matrix
- image4.png: System Architecture
- image5.png: Data Flow Analysis
- image6.png: 5x5 Risk Heatmap
- image7.png: Executive Dashboard / Risk Distribution
- image8.png: Pytest Terminal Output
"""

import os
import sys
import time
import subprocess
from playwright.sync_api import sync_playwright

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(ROOT_DIR, "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

def wait_for_streamlit_loaded(page, timeout=15000):
    page.wait_for_selector('[data-testid="stSidebar"]', timeout=timeout)
    # Wait for any spinners to disappear
    page.wait_for_selector('[data-testid="stSpinner"]', state="hidden", timeout=timeout)
    time.sleep(1.5)

def select_nav_page(page, label_text):
    # Click sidebar radio button matching label_text
    print(f"Navigating to page: '{label_text}'...")
    wait_for_streamlit_loaded(page)
    # Find radio item label containing label_text
    radio_locator = page.locator(f'label:has-text("{label_text}")')
    radio_locator.first.click()
    time.sleep(2.0)
    wait_for_streamlit_loaded(page)
    time.sleep(1.0)

def capture_ui_screenshots():
    print("Starting Playwright Edge session...")
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        # 1600x1050 viewport provides crisp, readable, unclipped academic layouts
        context = browser.new_context(viewport={"width": 1600, "height": 1050}, device_scale_factor=1.25)
        page = context.new_page()

        print("Navigating to http://localhost:8501...")
        page.goto("http://localhost:8501", wait_until="networkidle", timeout=30000)
        wait_for_streamlit_loaded(page)

        # -------------------------------------------------------------
        # 1. IMAGE 7: Dashboard (Executive KPIs & Risk Distribution)
        # -------------------------------------------------------------
        select_nav_page(page, "Dashboard")
        time.sleep(1.5)
        img7_path = os.path.join(SCREENSHOTS_DIR, "image7.png")
        page.screenshot(path=img7_path, full_page=False)
        print(f"Captured image7.png: Dashboard Overview -> {img7_path}")

        # -------------------------------------------------------------
        # 2. IMAGE 4: System Architecture
        # -------------------------------------------------------------
        select_nav_page(page, "System Architecture")
        time.sleep(1.5)
        img4_path = os.path.join(SCREENSHOTS_DIR, "image4.png")
        page.screenshot(path=img4_path, full_page=False)
        print(f"Captured image4.png: System Architecture -> {img4_path}")

        # -------------------------------------------------------------
        # 3. IMAGE 5: Data Flow Analysis
        # -------------------------------------------------------------
        select_nav_page(page, "Data Flow Analysis")
        time.sleep(1.5)
        img5_path = os.path.join(SCREENSHOTS_DIR, "image5.png")
        page.screenshot(path=img5_path, full_page=False)
        print(f"Captured image5.png: Data Flow Analysis -> {img5_path}")

        # -------------------------------------------------------------
        # 4. IMAGE 1: STRIDE Threat Model
        # -------------------------------------------------------------
        select_nav_page(page, "STRIDE Threat Model")
        time.sleep(1.5)
        img1_path = os.path.join(SCREENSHOTS_DIR, "image1.png")
        page.screenshot(path=img1_path, full_page=False)
        print(f"Captured image1.png: STRIDE Threat Model -> {img1_path}")

        # -------------------------------------------------------------
        # 5. IMAGE 2: Risk Analysis / Risk Simulator
        # -------------------------------------------------------------
        select_nav_page(page, "Risk Analysis")
        time.sleep(1.5)
        img2_path = os.path.join(SCREENSHOTS_DIR, "image2.png")
        page.screenshot(path=img2_path, full_page=False)
        print(f"Captured image2.png: Risk Simulator -> {img2_path}")

        # -------------------------------------------------------------
        # 6. IMAGE 6: Actual 5x5 Risk Heatmap
        # Scroll down on Risk Analysis page to center the 5x5 Heatmap
        # -------------------------------------------------------------
        print("Scrolling down to center 5x5 Risk Heatmap...")
        page.evaluate("window.scrollBy(0, 680)")
        time.sleep(1.5)
        img6_path = os.path.join(SCREENSHOTS_DIR, "image6.png")
        page.screenshot(path=img6_path, full_page=False)
        print(f"Captured image6.png: 5x5 Risk Heatmap -> {img6_path}")

        # -------------------------------------------------------------
        # 7. IMAGE 3: Mitigation Controls / Traceability Matrix
        # -------------------------------------------------------------
        select_nav_page(page, "Mitigation Controls")
        time.sleep(1.5)
        img3_path = os.path.join(SCREENSHOTS_DIR, "image3.png")
        page.screenshot(path=img3_path, full_page=False)
        print(f"Captured image3.png: Mitigation Controls & Traceability -> {img3_path}")

        browser.close()
        print("UI automation completed successfully!")

def capture_pytest_screenshot():
    """
    Renders the exact, live execution of pytest -v with clean terminal styling.
    """
    print("Executing live pytest -v suite...")
    venv_python = os.path.join(ROOT_DIR, ".venv", "Scripts", "python.exe")
    res = subprocess.run([venv_python, "-m", "pytest", "-v"], cwd=ROOT_DIR, capture_output=True, text=True)
    pytest_output = res.stdout
    print(f"Pytest return code: {res.returncode}")

    from PIL import Image, ImageDraw, ImageFont

    # Create terminal canvas
    width = 1500
    lines = [l for l in pytest_output.splitlines() if l.strip()]
    line_height = 24
    height = max(800, len(lines) * line_height + 140)

    img = Image.new("RGBA", (width, height), "#0d1117") # GitHub terminal dark
    draw = ImageDraw.Draw(img)

    # Window title bar
    draw.rectangle([(0, 0), (width, 42)], fill="#161b22")
    # Window buttons
    draw.ellipse([(16, 14), (28, 26)], fill="#ff5f56") # red
    draw.ellipse([(36, 14), (48, 26)], fill="#ffbd2e") # yellow
    draw.ellipse([(56, 14), (68, 26)], fill="#27c93f") # green

    # Load monospace font
    font = None
    for font_path in [
        "C:\\Windows\\Fonts\\consola.ttf",
        "C:\\Windows\\Fonts\\cour.ttf",
        "C:\\Windows\\Fonts\\lucon.ttf"
    ]:
        if os.path.exists(font_path):
            try:
                font = ImageFont.truetype(font_path, 15)
                title_font = ImageFont.truetype(font_path, 14)
                break
            except Exception:
                pass
    if font is None:
        font = ImageFont.load_default()
        title_font = font

    # Draw title
    draw.text((width // 2 - 160, 12), "PowerShell — pytest -v (Verification Suite)", fill="#8b949e", font=title_font)

    # Draw command prompt header
    y = 60
    prompt_line = "PS C:\\Users\\saran\\OneDrive\\Documents\\sem7\\DSP\\e2ee-ai-chatbot-threat-model> pytest -v"
    draw.text((30, y), prompt_line, fill="#58a6ff", font=font)
    y += line_height + 6

    for line in lines:
        fill_color = "#c9d1d9"
        if "PASSED" in line:
            # Highlight passed in bright terminal green
            parts = line.split("PASSED")
            draw.text((30, y), parts[0], fill="#8b949e", font=font)
            passed_x = 30 + int(draw.textlength(parts[0], font=font))
            draw.text((passed_x, y), "PASSED", fill="#3fb950", font=font)
            if len(parts) > 1:
                pct_x = passed_x + int(draw.textlength("PASSED", font=font))
                draw.text((pct_x, y), parts[1], fill="#58a6ff", font=font)
        elif "passed in" in line:
            draw.text((30, y), line, fill="#3fb950", font=font) # Green summary
        elif "test session starts" in line or "rootdir:" in line or "platform" in line:
            draw.text((30, y), line, fill="#8b949e", font=font)
        else:
            draw.text((30, y), line, fill=fill_color, font=font)
        y += line_height

    img8_path = os.path.join(SCREENSHOTS_DIR, "image8.png")
    img.save(img8_path, "PNG")
    print(f"Captured image8.png: Pytest Suite Terminal -> {img8_path}")

if __name__ == "__main__":
    capture_ui_screenshots()
    capture_pytest_screenshot()
    print("ALL 8 SCREENSHOTS CAPTURED SUCCESSFULLY!")
