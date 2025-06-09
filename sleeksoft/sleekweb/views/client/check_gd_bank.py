import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import random



def check_keyword_rank(keyword, domain, proxy=None, device='Desktop'):
    ua = UserAgent()

    results = []

    for page in range(10):  # 10 pages => 100 results
        user_agent = ua.chrome if device == 'Desktop' else ua.android
        headers = {
            "User-Agent": user_agent,
            "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://www.google.com/",
        }

        start = page * 10
        url = f"https://www.google.com.vn/search?q={requests.utils.quote(keyword)}&start={start}&hl=vi"

        try:
            response = requests.get(
                url,
                headers=headers,
                proxies={"http": proxy, "https": proxy} if proxy else None,
                timeout=10
            )
            if response.status_code != 200:
                print(f"❌ Lỗi HTTP {response.status_code} ở trang {page + 1}")
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            print("soup:",soup)
            blocks = soup.select('div.g')

            if not blocks:
                print("🔍 Không tìm thấy kết quả.")
                break

            for idx, block in enumerate(blocks):
                a_tag = block.select_one('a[href]')
                if not a_tag:
                    continue
                link = a_tag['href']
                rank = start + idx + 1
                results.append({'rank': rank, 'url': link})
                if domain in link:
                    return {
                        'keyword': keyword,
                        'domain': domain,
                        'rank': rank,
                        'url': link
                    }

            # Random delay
            time.sleep(random.uniform(2, 4))

        except Exception as e:
            print("⚠️ Lỗi:", e)
            break

    return {
        'keyword': keyword,
        'domain': domain,
        'rank': None,
        'url': None,
        'message': 'Không tìm thấy trong top 100'
    }


resul = check_keyword_rank('mua iphone 13 pro max', 'cellphones.com.vn', proxy=None, device='Desktop')
print('resul:',resul)