import os, re, sys, asyncio, json
from playwright.async_api import async_playwright
OUT = 'docs_out'; os.makedirs(OUT, exist_ok=True)
items = [l.split(None, 1) for l in open('docsfetch/urls.txt') if l.strip()]
log = {}
def pdf_text(path, dest):
    import subprocess
    subprocess.run(['pdftotext', '-layout', path, dest], check=False)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(accept_downloads=True, locale='pt-BR',
              user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36')
        for key, url in items:
            url = url.strip()
            try:
                if url.lower().split('?')[0].endswith('.pdf'):
                    r = await ctx.request.get(url, timeout=120000)
                    open(f'{OUT}/{key}.pdf', 'wb').write(await r.body())
                    pdf_text(f'{OUT}/{key}.pdf', f'{OUT}/{key}.txt')
                    log[key] = f'pdf {r.status} {len(await r.body())}'
                    continue
                pg = await ctx.new_page()
                await pg.goto(url, timeout=120000, wait_until='networkidle')
                await pg.wait_for_timeout(4000)
                txt = await pg.inner_text('body')
                open(f'{OUT}/{key}.txt', 'w').write(txt)
                links = await pg.eval_on_selector_all('a', 'els=>els.map(e=>[e.innerText.trim(), e.href])')
                json.dump(links, open(f'{OUT}/{key}.links.json', 'w'), ensure_ascii=False)
                log[key] = f'html {len(txt)}'
                if key == 'nscgj':
                    pdfs = [h for t, h in links if '.pdf' in h.lower()]
                    for i, h in enumerate(pdfs[:12]):
                        try:
                            r = await ctx.request.get(h, timeout=180000)
                            fn = f'{OUT}/nscgj_{i}.pdf'
                            open(fn, 'wb').write(await r.body())
                            pdf_text(fn, fn[:-4] + '.txt')
                            log[f'nscgj_{i}'] = f'{h} {r.status}'
                        except Exception as e:
                            log[f'nscgj_{i}'] = f'ERR {h} {e}'
                await pg.close()
            except Exception as e:
                log[key] = f'ERR {e}'
        await b.close()
    json.dump(log, open(f'{OUT}/_log.json', 'w'), indent=1, ensure_ascii=False)
    print(json.dumps(log, indent=1, ensure_ascii=False))
asyncio.run(main())
