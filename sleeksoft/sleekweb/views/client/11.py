import asyncio
from playwright.async_api import async_playwright
import random
import logging

logging.basicConfig(level=logging.INFO)

async def check_keyword_rank(keyword, domain, device='desktop', proxy=None, max_pages=10):
    results = []

    user_agents = {
        'desktop': [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        ],
        'mobile': [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36"
        ]
    }

    user_agent = random.choice(user_agents.get(device.lower(), user_agents['desktop']))
    logging.info(f"User-Agent: {user_agent}")

    async with async_playwright() as p:
        browser_args = []
        if proxy:
            browser_args = [f'--proxy-server={proxy}']

        browser = await p.chromium.launch(headless=True, args=browser_args)
        
        context = await browser.new_context(
            user_agent=user_agent,
            viewport={"width": 1280, "height": 720} if device.lower() == 'desktop' else {"width": 375, "height": 667},
            locale='vi-VN',
            java_script_enabled=True,
            device_scale_factor=2 if device.lower() == 'mobile' else 1,
            is_mobile=device.lower() == 'mobile',
            proxy={"server": proxy} if proxy else None,
        )
        page = await context.new_page()

        for page_num in range(max_pages):
            start = page_num * 10
            url = f"https://www.google.com.vn/search?q={keyword}&start={start}&hl=vi"
            logging.info(f"Truy cập: {url}")

            try:
                await page.goto(url, timeout=15000)

                html = await page.content()
                with open("output_google.html", "w", encoding="utf-8") as f:
                    f.write(html)

                await page.wait_for_selector('div.g', timeout=10000)


                results_blocks = await page.query_selector_all('div.g')

                if not results_blocks:
                    logging.warning("Không tìm thấy kết quả trên trang này.")
                    break

                for idx, block in enumerate(results_blocks):
                    a_tag = await block.query_selector('a[href]')
                    if not a_tag:
                        continue
                    link = await a_tag.get_attribute('href')
                    rank = start + idx + 1
                    results.append({'rank': rank, 'url': link})

                    if domain in link:
                        await browser.close()
                        logging.info(f"Tìm thấy domain '{domain}' ở vị trí {rank} với link {link}")
                        return {
                            'keyword': keyword,
                            'domain': domain,
                            'rank': rank,
                            'url': link
                        }

                delay = random.uniform(2, 5)
                logging.info(f"Delay {delay:.2f}s trước khi request trang tiếp theo...")
                await asyncio.sleep(delay)

            except Exception as e:
                logging.error(f"Lỗi khi truy cập hoặc lấy dữ liệu: {e}")
                break

        await browser.close()

    return {
        'keyword': keyword,
        'domain': domain,
        'rank': None,
        'url': None,
        'message': 'Không tìm thấy trong top 100 kết quả'
    }


if __name__ == "__main__":
    keyword = 'mua iphone 13 pro max'
    domain = 'cellphones.com.vn'

    result = asyncio.run(check_keyword_rank(keyword, domain, device='desktop', proxy=None))
    print('Kết quả:', result)
