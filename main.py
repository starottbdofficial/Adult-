import json
import requests
import re
from datetime import datetime

# ব্যাকআপ ইমেজের ইউআরএল
BACKUP_LOGO = "https://www.rexporn.st/static/pretty-girl-naomi-woods-is-already-an-adult-.-at-the-most-she-thinks-so.jpg"

def fetch_m3u(url):
    try:
        response = requests.get(url, timeout=15)
        return response.text
    except:
        return ""

def process_extinf(line):
    """#EXTINF লাইনে ব্যাকআপ লোগো যুক্ত করা এবং HTTP -> HTTPS করা"""
    line = line.replace("http://", "https://")
    
    # tvg-logo ট্যাগ আছে কিনা চেক করা
    match = re.search(r'tvg-logo="([^"]*)"', line)
    
    if match:
        logo_url = match.group(1).strip()
        # যদি tvg-logo খালি থাকে
        if not logo_url:
            line = re.sub(r'tvg-logo="[^"]*"', f'tvg-logo="{BACKUP_LOGO}"', line)
    else:
        # যদি tvg-logo ট্যাগটি একেবারেই না থাকে
        line = line.replace('#EXTINF:-1', f'#EXTINF:-1 tvg-logo="{BACKUP_LOGO}"')
        
    return line

def create_playlist():
    json_url = "http://plex.uskamlesh3.serv00.net/adult-movies.json"
    base_url = "https://plex.uskamlesh3.serv00.net/"
    
    playlist_1 = "http://adultiptv.net/chs.m3u"
    playlist_2 = "https://raw.githubusercontent.com/johirxofficial/otv-auto-updated-playlist/main/otv.m3u"
    
    output_file = "playlist.m3u"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # হেডার
        f.write("#EXTM3U\n")
        f.write(f"#EXTINF:-1,Playlist update: {now}\n")
        f.write("#EXTINF:-1,Playlist owner: STAR OTT BD\n")
        f.write("#EXTINF:-1,Playlist Creator: MD shakib Hasan\n")
        f.write("#EXTINF:-1,What's app: +8801610598422\n")
        f.write("#EXTINF:-1,Telegram: https://t.me/ibstvbd\n")
        f.write("#EXTINF:-1,Our official partner : IBS TV. STAR SHARE. OPPLEX.\n\n")
        
        # ১. প্রথম প্লেলিস্ট প্রসেসিং
        p1_content = fetch_m3u(playlist_1).replace("#EXTM3U", "").strip()
        p1_lines = p1_content.splitlines()
        for line in p1_lines:
            if line.startswith("#EXTINF"):
                f.write(process_extinf(line) + "\n")
            elif line.strip():
                f.write(line.replace("http://", "https://") + "\n")
        
        # ২. দ্বিতীয় প্লেলিস্ট প্রসেসিং ("XXX" ফিল্টার)
        otv_content = fetch_m3u(playlist_2)
        lines = otv_content.splitlines()
        for i in range(len(lines)):
            if "XXX" in lines[i] and lines[i].startswith("#EXTINF"):
                f.write(process_extinf(lines[i]) + "\n")
                if i + 1 < len(lines):
                    f.write(lines[i+1].replace("http://", "https://") + "\n")
        
        # ৩. মেইন JSON থেকে লোড
        try:
            response = requests.get(json_url, timeout=15)
            data = response.json()
            for item in data:
                name = item.get("name", "Unknown")
                logo = item.get("logo", "").strip()
                
                # লোগো না থাকলে বা খালি থাকলে ব্যাকআপ লোগো সেট করা
                if not logo:
                    logo = BACKUP_LOGO
                else:
                    logo = logo.replace("http://", "https://")
                
                url = item.get("direct_source", "").replace("[[SERVER_URL]]/", "").replace("[[SERVER_URL]]", "")
                full_url = base_url + url.lstrip('/')
                full_url = full_url.replace("http://", "https://")
                
                f.write(f'#EXTINF:-1 tvg-logo="{logo}",{name}\n{full_url}\n')
        except:
            pass

    print(f"প্লেলিস্ট সফলভাবে আপডেট হয়েছে: {now}")

if __name__ == "__main__":
    create_playlist()
    
