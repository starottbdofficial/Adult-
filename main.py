import json
import requests
from datetime import datetime

def fetch_m3u(url):
    try:
        response = requests.get(url, timeout=15)
        return response.text
    except:
        return ""

def create_playlist():
    # মেইন JSON সোর্স
    json_url = "http://plex.uskamlesh3.serv00.net/adult-movies.json"
    base_url = "http://plex.uskamlesh3.serv00.net/"
    
    # নতুন দুটি প্লেলিস্ট
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
        
        # ১. প্রথম প্লেলিস্ট লোড (সব কন্টেন্ট)
        f.write(fetch_m3u(playlist_1).replace("#EXTM3U", "") + "\n")
        
        # ২. দ্বিতীয় প্লেলিস্ট থেকে শুধু "XXX" গ্রুপ ফিল্টার করা
        otv_content = fetch_m3u(playlist_2)
        lines = otv_content.splitlines()
        for i in range(len(lines)):
            if "XXX" in lines[i] and lines[i].startswith("#EXTINF"):
                f.write(lines[i] + "\n")
                if i + 1 < len(lines):
                    f.write(lines[i+1] + "\n")
        
        # ৩. মেইন JSON থেকে লোড
        try:
            response = requests.get(json_url, timeout=15)
            data = response.json()
            for item in data:
                name = item.get("name", "Unknown")
                url = item.get("direct_source", "").replace("[[SERVER_URL]]/", "").replace("[[SERVER_URL]]", "")
                full_url = base_url + url.lstrip('/')
                f.write(f'#EXTINF:-1,{name}\n{full_url}\n')
        except:
            pass

    print(f"প্লেলিস্ট সফলভাবে আপডেট হয়েছে: {now}")

if __name__ == "__main__":
    create_playlist()
    
