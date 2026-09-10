"""Local browser checks. Requires Playwright and an installed Chrome browser.
Run: python tests/hvac_browser.py (serves repository on loopback only).
"""
from pathlib import Path
import functools
import http.server
import json
import threading
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.tmp/hvac-tools'))
from playwright.sync_api import sync_playwright

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT)))
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f'http://127.0.0.1:{server.server_port}'
out = ROOT / '.tmp/hvac-qa'
out.mkdir(exist_ok=True)
results = []
with sync_playwright() as p:
    browser = p.chromium.launch(channel='chrome', headless=True)
    page = browser.new_page()
    errors, failures, submissions, console_errors, network_errors = [], [], [], [], []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('console', lambda message: console_errors.append(message.text) if message.type == 'error' else None)
    page.on('requestfailed', lambda request: network_errors.append([request.url, request.failure]))
    page.on('response', lambda response: failures.append([response.url, response.status]) if response.status >= 400 else None)
    page.on('request', lambda request: submissions.append(request.url) if request.method != 'GET' else None)
    for width in [320, 375, 390, 430, 768, 1024, 1440]:
        page.set_viewport_size({'width': width, 'height': 1000})
        page.goto(base + '/en/demos/hvac/', wait_until='networkidle')
        for img in page.locator('img').all():
            img.scroll_into_view_if_needed()
            img.evaluate('(img) => img.decode()')
        page.evaluate('window.scrollTo(0,0)')
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'Overflow at {width}'
        assert page.locator('h1').count() == 1
        assert page.locator('meta[name="robots"]').get_attribute('content') == 'noindex, follow'
        assert page.locator('img').evaluate_all('(imgs) => imgs.every(i => i.complete && i.naturalWidth > 0)')
        if width <= 1100:
            page.get_by_role('button', name='Menu').click()
            assert page.locator('#main-nav').is_visible()
            page.locator('#main-nav').get_by_role('link', name='Services', exact=True).click()
            assert page.locator('.menu-toggle').get_attribute('aria-expanded') == 'false'
            page.get_by_role('button', name='Menu').click()
            page.keyboard.press('Escape')
            assert page.locator('.menu-toggle').get_attribute('aria-expanded') == 'false'
        page.evaluate('window.scrollTo(0,0)')
        page.screenshot(path=str(out / f'demo-{width}.png'), full_page=True)
        results.append({'width': width, 'overflow': False, 'images': 'pass', 'menu': 'pass'})
    # All local anchors and references on the demo resolve.
    anchors = page.locator('a[href^="#"]').evaluate_all('(links) => links.map(a => a.getAttribute("href").slice(1))')
    for anchor in anchors:
        assert page.locator(f'[id="{anchor}"]').count() == 1, anchor
    page.locator('[data-demo-call]').first.click()
    assert page.locator('#call-dialog').is_visible()
    page.keyboard.press('Escape')
    assert not page.locator('#call-dialog').is_visible()
    page.locator('[data-service="Furnace Repair"]').first.click()
    assert page.locator('#service').input_value() == 'Furnace Repair'
    page.locator('#submit-quote').click()
    assert page.locator('#form-status').inner_text() == ''
    for selector, value in {'#name':'Demo Visitor','#phone':'4035550148','#email':'demo@example.com','#postal':'T2P 1J9','#message':'Sample only'}.items():
        page.locator(selector).fill(value)
    page.locator('#submit-quote').click()
    assert 'No request was sent' in page.locator('#form-status').inner_text()
    assert page.locator('#name').input_value() == ''
    assert not submissions, submissions
    assert not errors, errors
    assert not failures, failures
    # True rendered preview, not a composited mockup.
    page.goto(base + '/en/demos/hvac/', wait_until='networkidle')
    page.screenshot(path=str(out / 'portfolio-preview.png'))
    from PIL import Image
    Image.open(out / 'portfolio-preview.png').convert('RGB').save(ROOT / 'en/demos/hvac/images/portfolio-preview.webp', 'WEBP', quality=85)
    nojs = browser.new_page(java_script_enabled=False)
    nojs.goto(base + '/en/demos/hvac/')
    assert nojs.locator('#submit-quote').is_disabled()
    assert nojs.locator('#main-nav').is_visible()
    nojs.close()
    demo_errors = list(errors)
    for width in [320, 375, 390, 430, 768, 1024, 1440]:
        page.set_viewport_size({'width': width, 'height': 1000})
        page.goto(base + '/en/portfolio/', wait_until='networkidle')
        page.locator('#footer footer').wait_for()
        assert page.locator('.container').first.evaluate('(el) => getComputedStyle(el).paddingLeft') != '0px', 'Bootstrap did not load'
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'Portfolio overflow at {width}'
        assert page.locator('a[href="/en/demos/hvac/"]').count() == 2
        if width == 390:
            page.locator('.navbar-toggler').click()
            page.locator('#navbarNavEn.show').wait_for(state='visible')
        page.locator('#hvac-concept').scroll_into_view_if_needed()
        page.screenshot(path=str(out / f'portfolio-{width}.png'), full_page=True)
    (out / 'results.json').write_text(json.dumps({'demo':results,'form':'pass, no network submission','demo_js_errors':demo_errors,'all_js_errors':errors,'http_failures':failures,'console_errors':console_errors,'network_errors':network_errors},indent=2),encoding='utf-8')
    print((out / 'results.json').read_text())
    browser.close()
server.shutdown()
