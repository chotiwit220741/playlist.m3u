import requests
import json
import re

def get_trueid_playlist():
    # Header จำลองการทำงานผ่านเบราว์เซอร์จริง
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'th-TH,th;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    # รายชื่อ Slugs ช่องสดหลักๆ ของ TrueID
    channel_slugs = [
        "33-hd", "mono29", "tnn16", "31-hd", "34-hd", "22-nationtv", 
        "23-workpoint", "24-true4u", "25-gmm25", "8-channel", "ch7-hd"
    ]

    m3u_output = ["#EXTM3U\n"]

    # ช่อง Static พื้นฐาน
    m3u_output.append('#EXTINF:-1 group-title="Digital TV", CH7 HD')
    m3u_output.append('https://live-cdn.ch7.com/out/v1/eafeb02c55b64a15b278b1e66c7fc776/playlist_13.m3u8\n')

    m3u_output.append('#EXTINF:-1 group-title="Digital TV", TV5 HD')
    m3u_output.append('https://639bc5877c5fe.streamlock.net/tv5hdlive/tv5hdlive/playlist.m3u8\n')

    print("Fetching TrueID channels...")
    for slug in channel_slugs:
        url = f"https://m.trueid.net/tv/live/{slug}"
        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                # ค้นหา Master Manifest URL
                match = re.search(r'https://cdn[0-9]+\.stm\.trueid\.net/[^"]+playlist\.m3u8\?[^"]+', res.text)
                if match:
                    stream_url = match.group(0)
                    ch_name = slug.replace("-", " ").upper()
                    m3u_output.append(f'#EXTINF:-1 group-title="TrueID", TrueID - {ch_name}')
                    m3u_output.append(f'{stream_url}\n')
                    print(f"Success: {slug}")
        except Exception as e:
            print(f"Failed {slug}: {e}")

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_output))

if __name__ == "__main__":
    get_trueid_playlist()
