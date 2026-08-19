import requests
from bs4 import BeautifulSoup
import re

def get_tvjaa_stream(channel_slug):
    url = f"https://tvjaa.com/tv/{channel_slug}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://tvjaa.com/'
    }
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            # ค้นหา URL .m3u8 ภายใน Source Code ของ TVJAA
            match = re.search(r'https?://[^\s\'"]+\.m3u8[^\s\'"]*', res.text)
            if match:
                return match.group(0)
    except Exception as e:
        print(f"Error fetching {channel_slug}: {e}")
    return None

def main():
    # รายชื่อช่องหลักบน TVJAA (Slug บน URL)
    channels = {
        "3HD": "ch3",
        "7HD": "ch7",
        "Mono29": "mono29",
        "One31": "one31",
        "ThairathTV": "thairath32",
        "AmarinTV": "amarin34",
        "Workpoint": "workpoint",
        "GMM25": "gmm25",
        "TNN16": "tnn16",
        "PPTV": "pptv36"
    }

    m3u_output = ["#EXTM3U\n"]

    print("Fetching streams from TVJAA...")
    for name, slug in channels.items():
        stream_url = get_tvjaa_stream(slug)
        if stream_url:
            m3u_output.append(f'#EXTINF:-1 group-title="TVJAA", {name}')
            m3u_output.append(f'{stream_url}\n')
            print(f"Success: {name}")
        else:
            print(f"Failed: {name}")

    # บันทึกไฟล์ playlist.m3u
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_output))

if __name__ == "__main__":
    main()
