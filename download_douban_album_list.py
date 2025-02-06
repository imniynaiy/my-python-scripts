import re
import time
import requests

# Path to the file containing the HTML content
file_path = '/Users/kokugo/Downloads/endo_sakura/other.md'

# Read the content of the file
with open(file_path, 'r') as file:
    content = file.read()

# Regex pattern to find all .webp links
pattern = r'https?://[^\s"]+\.webp'

# Find all .webp links in the content
webp_links = re.findall(pattern, content)

# Download each .webp file
for link in webp_links:
    time.sleep(1)
    response = requests.get(link)
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
        'cache-control': 'max-age=0',
        'if-modified-since': 'Thu, 04 Jan 2024 09:03:43 GMT',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
    }

    response = requests.get(link, headers=headers)
    if response.status_code == 200:
        file_name = link.split('/')[-1]
        with open("downloaded_l/other/"+file_name, 'wb') as f:
            f.write(response.content)
        print(f'Downloaded: {file_name}')
    else:
        print(f'Failed to download: {link}')