from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

from playwright.sync_api import Page, sync_playwright


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    result.add_argument("--url", default="http://127.0.0.1:8042")
    result.add_argument("--ffmpeg", type=Path, required=True)
    return result


def wait_for_status(page: Page, status: str) -> None:
    page.locator("#status").filter(has_text=status).wait_for(timeout=8_000)


def render_success(page: Page) -> None:
    page.locator("#recipe-form button[type=submit]").click()
    wait_for_status(page, "succeeded")
    page.locator("#preview img").wait_for()


def render_failure(page: Page) -> None:
    page.locator("#simulate-failure").check()
    page.locator("#recipe-form button[type=submit]").click()
    wait_for_status(page, "failed")
    page.locator("#error-panel").wait_for()


def capture_images(page: Page, output: Path, url: str) -> None:
    page.goto(url, wait_until="networkidle")
    render_success(page)
    page.evaluate("scrollTo(0, 0)")
    page.screenshot(path=output / "01_cover.png")

    page.locator("#workflow-proof").scroll_into_view_if_needed()
    page.screenshot(path=output / "02_workflow.png")

    page.evaluate("scrollTo(0, 0)")
    render_failure(page)
    page.evaluate("scrollTo(0, 0)")
    page.screenshot(path=output / "03_recovery.png")


def capture_responsive(browser: object, root: Path, url: str) -> None:
    screenshots = root / "docs" / "screenshots"
    for width, height in ((1440, 900), (1024, 900), (390, 844)):
        page = browser.new_page(viewport={"width": width, "height": height})
        page.goto(url, wait_until="networkidle")
        render_success(page)
        page.evaluate("scrollTo(0, 0)")
        page.screenshot(path=screenshots / f"printline-workstation-{width}.png")
        page.close()


def inject_tour(page: Page) -> None:
    page.evaluate(
        """
        () => {
          const style = document.createElement('style');
          style.textContent = `
            #tour-caption { position:fixed; left:50%; top:30px; transform:translateX(-50%); z-index:9998; width:min(1060px,78vw); padding:17px 25px; color:white; background:#171918; border:1px solid white; box-shadow:8px 8px 0 #ff5b45; font:750 27px/1.2 "Segoe UI",sans-serif; text-align:center; opacity:0; transition:opacity .25s ease; }
            #tour-cursor { position:fixed; left:120px; top:110px; z-index:9999; width:29px; height:29px; border:3px solid white; border-radius:50%; background:#6653f5; box-shadow:0 2px 12px #0008; pointer-events:none; transition:left .55s ease, top .55s ease, transform .15s ease; }
            #tour-end { position:fixed; inset:0; z-index:10000; display:grid; place-items:center; color:white; background:#171918; opacity:0; pointer-events:none; transition:opacity .35s ease; }
            #tour-end div { width:min(980px,82vw); text-align:center; }
            #tour-end small { color:#ff7a66; font:800 13px/1 "Courier New",monospace; letter-spacing:.14em; }
            #tour-end h2 { margin:20px 0; font-size:65px; line-height:.95; letter-spacing:-.055em; }
            #tour-end p { margin:0; color:#c7ccc8; font-size:22px; }
          `;
          document.head.append(style);
          const caption = document.createElement('div'); caption.id='tour-caption'; document.body.append(caption);
          const cursor = document.createElement('div'); cursor.id='tour-cursor'; document.body.append(cursor);
          const end = document.createElement('div'); end.id='tour-end'; end.innerHTML='<div><small>PRINTLINE</small><h2>Queue the graph. Inspect the artifact. Recover the run.</h2><p>ComfyUI-compatible graph · provenance · failure state · retry lineage</p></div>'; document.body.append(end);
        }
        """
    )


def caption(page: Page, value: str) -> None:
    page.evaluate(
        "value => { const node=document.querySelector('#tour-caption'); node.textContent=value; node.style.opacity='1'; }",
        value,
    )


def move_cursor(page: Page, selector: str) -> None:
    box = page.locator(selector).bounding_box()
    if box is None:
        return
    page.evaluate(
        "point => { const node=document.querySelector('#tour-cursor'); node.style.left=`${point.x}px`; node.style.top=`${point.y}px`; }",
        {"x": box["x"] + box["width"] * 0.72, "y": box["y"] + box["height"] * 0.45},
    )


def capture_video(page: Page, url: str) -> None:
    page.goto(url, wait_until="networkidle")
    inject_tour(page)
    page.wait_for_timeout(1100)
    caption(page, "A recipe compiles into a parameterized ComfyUI API-format graph.")
    move_cursor(page, "#recipe-form button[type=submit]")
    page.wait_for_timeout(800)
    page.locator("#recipe-form button[type=submit]").click()
    wait_for_status(page, "succeeded")
    page.locator("#preview img").wait_for()
    page.wait_for_timeout(1800)

    caption(
        page,
        "The run records queue state, graph digest, artifact SHA and adapter boundary.",
    )
    page.locator("#workflow-proof").scroll_into_view_if_needed()
    page.wait_for_timeout(3000)

    page.evaluate("scrollTo({top:0,behavior:'smooth'})")
    page.wait_for_timeout(1000)
    caption(
        page, "A provider stop stays visible and produces an actionable retry path."
    )
    move_cursor(page, "#simulate-failure")
    page.wait_for_timeout(700)
    page.locator("#simulate-failure").check()
    move_cursor(page, "#recipe-form button[type=submit]")
    page.wait_for_timeout(650)
    page.locator("#recipe-form button[type=submit]").click()
    wait_for_status(page, "failed")
    page.wait_for_timeout(1800)

    caption(
        page, "Retry creates a linked run while preserving the failed run as evidence."
    )
    move_cursor(page, "#retry-button")
    page.wait_for_timeout(750)
    page.locator("#retry-button").click()
    wait_for_status(page, "succeeded")
    page.wait_for_timeout(2200)

    page.evaluate("document.querySelector('#tour-end').style.opacity='1'")
    page.wait_for_timeout(2400)


def main() -> int:
    arguments = parser().parse_args()
    root = Path(__file__).resolve().parents[1]
    output = root / "final_upload"
    video_tmp = root / ".capture_video"
    output.mkdir(exist_ok=True)
    if video_tmp.exists():
        shutil.rmtree(video_tmp)
    video_tmp.mkdir()

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        image_page = browser.new_page(viewport={"width": 1600, "height": 1200})
        capture_images(image_page, output, arguments.url)
        capture_responsive(browser, root, arguments.url)
        browser.close()

        context = playwright.chromium.launch(headless=True).new_context(
            viewport={"width": 1600, "height": 1200},
            record_video_dir=video_tmp,
            record_video_size={"width": 1600, "height": 1200},
        )
        video_page = context.new_page()
        capture_video(video_page, arguments.url)
        video = video_page.video
        context.close()
        source = video.path()

    subprocess.run(
        [
            str(arguments.ffmpeg),
            "-y",
            "-i",
            str(source),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(output / "04_printline_walkthrough.mp4"),
        ],
        check=True,
        capture_output=True,
    )
    shutil.rmtree(video_tmp)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
