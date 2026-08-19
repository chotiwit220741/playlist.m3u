import requests
import json

def fetch_all_trueid_channels():
    # API ของ TrueID สำหรับดึงข้อมูลรายการทีวีสดพร้อม Metadata
    api_url = "https://tv.trueid.net/api/v2/tv/channels"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }
    
    channels_data = []
    
    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            # วนลูปอ่านรายการช่องทั้งหมดจาก JSON
            for item in data.get('data', []):
                title = item.get('title', '').strip()
                slug = item.get('slug', '')
                logo = item.get('thumb_logo', '') or item.get('logo', '')
                
                if slug:
                    # ดึง Stream URL ติด Token ของช่องนั้นๆ
                    stream_url = get_channel_stream_url(slug, headers)
                    if stream_url:
                        channels_data.append({
                            'title': title,
                            'logo': logo,
                            'url': stream_url
                        })
    except Exception as e:
        print(f"Error fetching channel list: {e}")
        
    return channels_data

def get_channel_stream_url(slug, headers):
    # ยิง Request เข้าหน้าช่องเพื่อสกัด Master Playlist URL
    page_url = f"https://m.trueid.net/tv/live/{slug}"
    try:
        res = requests.get(page_url, headers=headers, timeout=10)
        import re
        # ดึง URL ที่ลงท้ายด้วย playlist.m3u8 พร้อม Token
        match = re.search(r'https://cdn[0-9]+\.stm\.trueid\.net/[^"]+playlist\.m3u8\?[^"]+', res.text)
        if match:
            return match.group(0)
    except Exception:
        pass
    return None

# --- Main Process ---
print("Fetching live channels from TrueID...")
live_channels = fetch_all_trueid_channels()

# สร้างโครงสร้างไฟล์ M3U
m3u_lines = ["#EXTM3U\n"]

# เพิ่มช่องฟรีทีวีหลัก (Static CDN)
m3u_lines.append('#EXTINF:-1 group-title="Digital TV", CH7 HD')
m3u_lines.append('https://live-cdn.ch7.com/out/v1/eafeb02c55b64a15b278b1e66c7fc776/playlist_13.m3u8\n')

m3u_lines.append('#EXTINF:-1 group-title="Digital TV", TV5 HD')
m3u_lines.append('https://639bc5877c5fe.streamlock.net/tv5hdlive/tv5hdlive/playlist.m3u8\n')

# เพิ่มช่องทั้งหมดที่ดึงมาจาก TrueID
for ch in live_channels:
    logo_attr = f' tvg-logo="{ch["logo"]}"' if ch["logo"] else ''
    m3u_lines.append(f'#EXTINF:-1 group-title="TrueID"{logo_attr}, {ch["title"]}')
    m3u_lines.append(f'{ch["url"]}\n')

# เขียนทับลงไฟล์ playlist.m3u
with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(m3u_lines))

print(f"Done! Successfully generated {len(live_channels)} TrueID channels.")
