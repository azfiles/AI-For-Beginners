"""Execute every browser-supported notebook in Chromium's actual Pyodide kernel."""
import functools, http.server, json, threading, time
from pathlib import Path
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1]
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root / 'lite-dist'))
server = http.server.ThreadingHTTPServer(('127.0.0.1', 8765), handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
specs = json.loads((root / 'website/browser-notebooks.json').read_text())
results = []
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for path in specs:
            page = browser.new_page()
            page.set_default_timeout(600000)
            started = time.monotonic()
            try:
                page.goto('http://127.0.0.1:8765/lab/index.html?path=' + path)
                page.wait_for_function('window.jupyterapp && window.jupyterapp.shell.currentWidget && window.jupyterapp.shell.currentWidget.context', timeout=120000)
                page.evaluate('''async () => {
                    const app = window.jupyterapp;
                    await app.restored;
                    const panel = app.shell.currentWidget;
                    await panel.context.ready;
                    await panel.sessionContext.ready;
                }''')
                page.evaluate("window.jupyterapp.commands.execute('notebook:run-all-cells')")
                page.wait_for_function('''() => {
                    const panel = window.jupyterapp.shell.currentWidget;
                    const cells = panel.content.model.toJSON().cells.filter(c => c.cell_type === 'code' && c.source.trim());
                    return cells.some(c => c.outputs.some(o => o.output_type === 'error')) ||
                        (cells.every(c => c.execution_count !== null) && panel.sessionContext.session.kernel.status === 'idle');
                }''', timeout=600000)
                cells = page.evaluate('window.jupyterapp.shell.currentWidget.content.model.toJSON().cells')
                errors = [o for c in cells for o in c.get('outputs', []) if o.get('output_type') == 'error']
                assert not errors, str(errors)
                result = {'path': path, 'status': 'passed', 'executed_cells': sum(c.get('execution_count') is not None for c in cells)}
            except Exception as exc:
                result = {'path': path, 'status': 'failed', 'error': str(exc)}
                page.screenshot(path=str(root / ('browser-failure-' + str(len(results)) + '.png')))
            result['seconds'] = round(time.monotonic() - started, 1)
            results.append(result)
            (root / 'browser-results.json').write_text(json.dumps(results, indent=2))
            print(json.dumps(result), flush=True)
            page.close()
        browser.close()
finally:
    server.shutdown()
assert all(r['status'] == 'passed' for r in results), results
