#!/usr/bin/env python3
import requests
import re
import sys

# Thông tin từ link của bạn
USERNAME = "jjyw70ss4w"
PASSWORD = "ek5ui8ithc"
PANEL_URL = "http://best-8k.org"
OUTPUT_FILE = "iptv_safe_playlist.m3u"

def sanitize(text):
    """Làm sạch tên kênh và chuyên mục để tránh lỗi định dạng."""
    text = re.sub(r'[#\s]+$', '', str(text).strip())
    return re.sub(r'[\\/*?:"<>|]', "", text)

def main():
    print("Đang lấy danh sách chuyên mục (categories)...")
    cat_resp = requests.get(f"{PANEL_URL}/player_api.php", params={
        "username": USERNAME, "password": PASSWORD, "action": "get_live_categories"
    }, timeout=15)
    cat_resp.raise_for_status()
    categories = {str(cat["category_id"]): sanitize(cat["category_name"]) for cat in cat_resp.json()}

    print("Đang lấy danh sách kênh (streams)...")
    stream_resp = requests.get(f"{PANEL_URL}/player_api.php", params={
        "username": USERNAME, "password": PASSWORD, "action": "get_live_streams"
    }, timeout=15)
    stream_resp.raise_for_status()
    streams = stream_resp.json()

    print(f"Tìm thấy {len(streams)} kênh. Đang tạo file M3U...")
    m3u_lines = ["#EXTM3U"]
    for stream in streams:
        name = sanitize(stream["name"])
        group = categories.get(str(stream.get("category_id")), "General")
        # Sử dụng định dạng .m3u8 hoặc .ts tùy hệ thống, Xtream thường hỗ trợ cả hai
        stream_url = f"{PANEL_URL}/live/{USERNAME}/{PASSWORD}/{stream['stream_id']}.m3u8"
        m3u_lines.append(f'#EXTINF:-1 group-title="{group}",{name}')
        m3u_lines.append(stream_url)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_lines))

    print(f"Thành công! Đã lưu playlist tại file: {OUTPUT_FILE}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Lỗi: {e}")
        sys.exit(1)
