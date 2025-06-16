from googlesearch import search

proxy = ''

def check_rank(domain, keyword, max_results=100):
    for index, url in enumerate(search(keyword, num_results=max_results)):
        if domain in url:
            return index + 1
    return None

domain = "nikio.com.vn"
keyword = "May massage bụng"
rank = check_rank(domain, keyword)

if rank:
    print(f"Website xuất hiện ở vị trí thứ {rank}")
else:
    print("Không tìm thấy website trong top 100")


