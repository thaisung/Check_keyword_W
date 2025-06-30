# import requests
# from urllib.parse import urlparse
# import threading

# # Hàm gọi API
# def get_google_results(api_key, query, start, device):
#     url = "https://serpapi.com/search.json"
#     params = {
#         "engine": "google",
#         "q": query,
#         "hl": "vi",
#         "gl": "vn",
#         "start": start,
#         "device": device,
#         "api_key": api_key
#     }
#     response = requests.get(url, params=params)
#     response.raise_for_status()
#     return response.json().get("organic_results", [])

# # Biến toàn cục để lưu vị trí
# found_position = None
# lock = threading.Lock()

# # Hàm chạy cho từng trang
# def check_page(api_key, query, device, target_domain, start):
#     global found_position
#     try:
#         results = get_google_results(api_key, query, start, device)
#         for result in results:
#             link = result.get("link", "")
#             domain = urlparse(link).netloc.replace("www.", "")
#             if domain == target_domain:
#                 with lock:
#                     # Nếu đã tìm thấy trước đó thì không cần update
#                     if found_position is None:
#                         found_position = result["position"] + start
#     except Exception as e:
#         print(f"Error at start={start}: {e}")

# # Hàm chính chạy đa luồng
# def find_domain_in_top_100(api_key, query, device, target_domain):
#     threads = []
#     for start in range(0, 100, 10):
#         thread = threading.Thread(
#             target=check_page,
#             args=(api_key, query, device, target_domain, start)
#         )
#         threads.append(thread)
#         thread.start()

#     for thread in threads:
#         thread.join()

#     return found_position or 'Không xác định'

# api_key = "6e24e8f8bd925f373026aae85e125972d6263fd9891420631cffb4728b9138d1"
# query = "Đai massage bụng"
# device = "desktop"
# target_domain = "dungcuytecantho.com"

# position = find_domain_in_top_100(api_key, query, device, target_domain)
# print(f"Tên miền '{target_domain}' nằm ở vị trí: {position}")



# import requests

# url = "https://api.apyhub.com/extract/serp/rank?language=vi&location=vn&size=100"
# headers = {
#     "Content-Type": "application/json",
#     "apy-token": "APY0QTxUdWvAzyW4RSxapCScmvbCM1cqvEUNuiTIx9oDBOTwFnT65iYsN8M3rba3n1e6fSHUES3DG1"
# }
# payload = {
#     "keyword": "apyhub"
# }

# response = requests.post(url, headers=headers, json=payload)

# # In kết quả JSON ra màn hình
# print(response.status_code)
# print(response.json())

from serpapi import GoogleSearch

SERPAPI_KEY = "0432911de80e522f03ffc76cf4b70bf4e771019b9afb49e7e86e57cf4af14901"

def get_rank_serpapi(keyword, domain, max_results=100):
    params = {
        "q": keyword,
        "num": 100,
        "api_key": SERPAPI_KEY,
        "engine": "google",
        "hl": "vi",
        "gl" : "vn",
        "device": "desktop"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    if "organic_results" not in results:
        print("Không có kết quả trả về.")
        return None

    for idx, item in enumerate(results["organic_results"], start=1):
        link = item.get("link", "")
        if domain in link:
            return idx

    return None

# Ví dụ sử dụng
keywords = ["Đai massage bụng"]
target_domain = "dienmayxanh.com"

for kw in keywords:
    print(f"\n🔎 Tìm từ khóa: {kw}")
    rank = get_rank_serpapi(kw, target_domain)
    if rank:
        print(f"✅ Domain nằm ở vị trí: {rank}")
    else:
        print("❌ Không tìm thấy trong top 100")
